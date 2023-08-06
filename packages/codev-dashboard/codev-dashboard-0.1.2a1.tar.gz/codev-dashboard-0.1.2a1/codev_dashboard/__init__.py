from datetime import datetime

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from collections import namedtuple

#### CONFIGURATION ####
import configparser
import os


class Configuration(object):
    def __init__(self):
        # general config
        config = configparser.ConfigParser()

        #defaults
        config.add_section('database')
        config.set('database', 'uri', 'sqlite:////tmp/codev_dashboard.db')

        config.read('/etc/codev-dashboard/config.ini')
        config.read(os.path.expanduser('~/.config/codev-dashboard/config.ini'))
        self.database = config['database']

        # projects
        projects = configparser.ConfigParser()
        projects.read('/etc/codev-dashboard/projects.ini')
        projects.read(os.path.expanduser('~/.config/codev-dashboard/projects.ini'))

        self.projects = {
            name: list(map(str.strip, projects[name]['environments'].split(',')))
            for name in projects.sections()
        }

#######################

CONFIGURATION = Configuration()

Deployment = namedtuple('Deployment', [
    'project', 'environment', 'infrastructure',
    'installation', 'installation_options', 'next_installation', 'next_installation_options'
])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIGURATION.database['uri']
db = SQLAlchemy(app)


class DeploymentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    project = db.Column(db.String(80))
    environment = db.Column(db.String(80))
    infrastructure = db.Column(db.String(80))
    installation = db.Column(db.String(80))
    installation_options = db.Column(db.String(80))
    next_installation = db.Column(db.String(80))
    next_installation_options = db.Column(db.String(80))
    is_ok = db.Column(db.Boolean)
    error = db.Column(db.Text)

    def __init__(self, project, environment, infrastructure, installation, installation_options, next_installation, next_installation_options, is_ok, error):
        self.project = project
        self.environment = environment
        self.infrastructure = infrastructure
        self.installation = installation
        self.installation_options = installation_options
        self.next_installation = next_installation
        self.next_installation_options = next_installation_options
        self.is_ok = is_ok
        self.error = error
        self.created = datetime.utcnow()

    @classmethod
    def add_success(cls, project, environment, infrastructure, installation, installation_options, next_installation, next_installation_options):
        return cls(project, environment, infrastructure, installation, installation_options, next_installation, next_installation_options, True, '')

    @classmethod
    def add_failure(cls, project, environment, infrastructure, installation, installation_options, next_installation, next_installation_options, error=''):
        return cls(project, environment, infrastructure, installation, installation_options, next_installation, next_installation_options, False, error)

    def __repr__(self):
        return '<{cls} {self.project}, {self.environment}, {self.infrastructure}, {self.installation_with_options}, {self.next_installation_with_options}>'.format(
            cls=self.__class__.__name__,
            self=self
        )

    def get_installation_with_options(self, nexti=False):
        return '{installation}:{installation_options}'.format(
            installation=self.next_installation if nexti else self.installation,
            installation_options=self.next_installation_options if nexti else self.installation_options
        )

    @property
    def installation_with_options(self):
        return self.get_installation_with_options()

    @property
    def next_installation_with_options(self):
        return self.get_installation_with_options(True)


DeploymentResult.next_result_id = db.Column(db.Integer, db.ForeignKey(DeploymentResult.id))
DeploymentResult.next_result = db.relationship(DeploymentResult, backref=db.backref('source_result', uselist=False), remote_side=DeploymentResult.id, uselist=False)


class Pipeline(object):
    def __init__(self, infrastructure, installation, last_change, deployment_results=[]):
        self.infrastructure = infrastructure
        self.installation = installation
        self.last_change = last_change
        self.deployment_results = deployment_results

    @property
    def error(self):
        # final result is not ok - possibly production error
        last_result = self.deployment_results[-1]
        if last_result is not None and not last_result.is_ok:
            return True
        else:
            return False

    @property
    def warning(self):
        # not error
        if self.error:
            return False

        for result in self.deployment_results:
            if result is not None and not result.is_ok:
                return True

        return False

    @property
    def success(self):
        for result in self.deployment_results:
            if result is None or not result.is_ok:
                return False
        return True

Project = namedtuple('Project', ['pipelines', 'environments'])


@app.route('/')
def index():
    projects = {}
    for project, environments in CONFIGURATION.projects.items():
        pipelines = []
        for dr in DeploymentResult.query.filter(
            DeploymentResult.project == project,
            DeploymentResult.environment.in_(environments)
        ).order_by(
            DeploymentResult.created.desc()
        ).filter_by(next_result=None).all():
            installation_with_options = dr.installation_with_options if dr.installation else dr.next_installation_with_options
            pipeline = Pipeline(dr.infrastructure, installation_with_options, dr.created, [])
            pipeline.deployment_results = [None] * len(environments)
            pipeline.deployment_results[environments.index(dr.environment)] = dr
            while dr.source_result:
                pipeline.deployment_results[environments.index(dr.source_result.environment)] = dr.source_result
                dr = dr.source_result
            pipelines.append(pipeline)
        projects[project] = Project(
            pipelines=pipelines,
            environments=environments
        )
    return render_template('index.html', projects=projects)


def get_deployment():
    project = request.form['project']
    environment = request.form['environment']
    infrastructure = request.form['infrastructure']
    installation = request.form['installation']
    installation_options = request.form['installation_options']
    next_installation = request.form['next_installation']
    next_installation_options = request.form['next_installation_options']

    return Deployment(
        project, environment, infrastructure,
        installation, installation_options, next_installation, next_installation_options
    )


@app.route('/add_success/', methods=['POST'])
def add_success():
    deployment = get_deployment()
    project = deployment.project
    source_result_query = DeploymentResult.query.filter_by(
        project=project,
        infrastructure=deployment.infrastructure,
    ).order_by(DeploymentResult.created.desc()).filter_by(next_result=None)

    source_result = source_result_query.filter_by(
        next_installation=deployment.installation,
        next_installation_options=deployment.installation_options
    ).first() or source_result_query.filter_by(
        installation=deployment.installation,
        installation_options=deployment.installation_options,
        next_installation=''
    ).first()

    if source_result:
        environments = CONFIGURATION.projects[project]
        current_environment_position = environments.index(deployment.environment)
        source_environment_position = environments.index(source_result.environment)

        if current_environment_position != source_environment_position + 1:
            source_result = None

    dr = DeploymentResult.add_success(*deployment)
    if source_result:
        source_result.next_result = dr
        db.session.add(source_result)
    db.session.add(dr)
    db.session.commit()
    return 'OK'


@app.route('/add_failure/', methods=['POST'])
def add_failure():
    error = request.form['error']
    dr = DeploymentResult.add_failure(*get_deployment(), error=error)
    db.session.add(dr)
    db.session.commit()
    return 'OK'
