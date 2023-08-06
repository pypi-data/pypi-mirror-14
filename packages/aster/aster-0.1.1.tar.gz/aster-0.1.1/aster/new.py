from os.path import join, basename
import aster
from aster.helpers import *
from aster import g
import aster.main

def create_files(name):
    for path in ['api', 'public', 'config', 'assets']:
        doing('MKDIR', path)
        os.makedirs(path)
        create_file(join(path, '.keep'), '')

    create_file(join('.gitignore'), '''\
/vendor
/tmp
/node_modules
/public/assets
*.pyc
''')

    create_file(join('assets', 'application.js'), '''\
''')

    create_file(join('README.md'), '''\
{name}
======
'''.format(**locals()))

    create_file(join('config', 'application.yml'), '''\
name: {name}
memory_size: 128

backend:
  name: aws

aws:
  lambda_iam: SETME
  s3_assets_bucket: SETME
'''.format(**locals()))

    create_file(join('requirements.txt'), '''\
aster
''')

    create_file(join('api', 'hello.py'), '''\
"""

  Hello World!

"""
from aster.support import jsonify

def get(request):
    print('Hello World!')
    return jsonify(request)
''')


def init_git():
    doing('GIT INIT')
    cmd(['git', 'init'])


def init_npm():
    doing('NPM INIT')
    cmd(['npm', 'init', '-y'])

    packages = [
        'del',
        'run-sequence',
        'babel',
        'babel-core',
        'babel-preset-es2015',
        'babel-loader',
        'gulp', 
        'gulp-rev',
        'gulp-scss',
        'gulp-minify-css',
        'gulp-webpack',
        'gulp-uglify',
        'gulp-babel'
    ]

    doing('NPM INSTALL', 'gulp babel webpack scss')
    cmd(['npm', 'install', '--save-dev'] + packages)

    create_file('gulpfile.js', '''\
var del  = require("del");
var gulp = require("gulp");
var scss = require("gulp-scss");
var rev  = require("gulp-rev");
var minifycss   = require("gulp-minify-css");
var uglify      = require("gulp-uglify");
var webpack     = require("gulp-webpack");
var runsequence = require("run-sequence");

var assets_dir  = "./assets";
var css_assets  = assets_dir + "/**/*.scss";
var js_assets   = assets_dir + "/**/*.js";

var public_dir = "./public/assets";
var css_public_dir       = public_dir + "/stylesheets";
var js_public_dir        = public_dir + "/javascripts";
var manifest_public_path = public_dir + "/manifest.json";

var manifest_options = {
    base: public_dir,
    merge: true
};

var webpack_options = {
    entry: {
	application: assets_dir + "/application"
    },

    output: {
        filename: "[name].js",
        publicPath: js_public_dir,
    },

    resolve: {
	extension: [".js"]
    },

    module: {
       loaders: [{
           test: /\.js$/,
           loader: "babel?presets[]=es2015"
       }]
    }
};

gulp.task("clean", function() {
    return del("public_dir");
});


gulp.task("css", function() {
    return gulp.src(css_assets)
             .pipe(scss({ errLogToConsole: true }))
             .pipe(minifycss())
             .pipe(rev())
             .pipe(gulp.dest(css_public_dir))
             .pipe(rev.manifest(manifest_public_path, manifest_options))
             .pipe(gulp.dest(public_dir));
});


gulp.task("js", function() {
    return gulp.src(js_assets)
             .pipe(webpack(webpack_options))
             .pipe(uglify())
             .pipe(rev())
             .pipe(gulp.dest(js_public_dir))
             .pipe(rev.manifest(manifest_public_path, manifest_options))
             .pipe(gulp.dest(public_dir));
});


gulp.task("watch", function() {
    gulp.watch(css_assets, ['css']);
    gulp.watch(js_assets, ['js']);
});


gulp.task("default", function() {
    runsequence(
      "clean",
      ["css", "js"]
    );
});
''')


def init_venv():
    doing('VENV INIT', 'vendor')
    cmd(['virtualenv', 'vendor'])


def install_requirements():
    doing('PIP INSTALL')
    aster.main.main(['install'])


def main():
    name = basename(g.args.path)
    
    plan('Creating a project template')
    doing('MKDIR', g.args.path)
    os.makedirs(g.args.path)
    os.chdir(g.args.path)
    init_git()
    create_files(name)
    init_npm()
    init_venv()
    install_requirements()
    plan('Have fun!')
