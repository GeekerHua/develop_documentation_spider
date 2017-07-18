from fabric.api import local

def prepare_deploy():
    local('python mainSpider.py')
    local('echo "haha"')
