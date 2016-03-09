from git import (Repo, Actor)
import logging
import arrow
import os
import config


logger = logging.getLogger(__name__)
"""
RepoManager takes care of the repository operations such as
 - creating/opening a repo
 - generating change
 - committing with date
 - pushing
"""
class RepoManager(object):

    """
    RepoManager with set up date

    :param path: set a specific path to repo
    """
    def __init__(self, path=os.getcwd()):
        self.path = os.path.abspath(path)
        self.author = Actor(config.COMMIT_AUTHOR['full_name'], config.COMMIT_AUTHOR['email'])
        self.commit_file = os.path.join(self.path, config.COMMIT_FILE)

    """
    Open existing repo passed in the constructor
    """
    def open_repo(self):
        if self.check_rights and os.path.isdir(os.path.join(self.path, '.git')):
            self.repo = Repo(self.path)
            return self.repo != None

        return False

    """
    Create new repo from the path passed in the constructor.

    :return: true if new repo created
    """
    def create_repo(self):
        if not os.path.isdir(os.path.join(self.path, '.git')):
            try:
                os.mkdir(self.path)
                self.repo = Repo.init(self.path)
                return True
            except (IOError, OSError) as e:
                logger.error('create_repo(%s) - %s', self.path, e)
        else:
            self.repo = Repo(self.path)

        return False

    """
    Generate change to the COMMIT_FILE in order to create a commit.
    """
    def generate_change(self):
        logger.info('Generating Change > %s ', self.commit_file)
        try:
            commit_file = open(self.commit_file, 'w')
            # write a predefined value to the file
            commit_file.write(config.COMMIT_VALUE)
            return True
        except (IOError, OSError) as e:
            logger.error('generate_change(%s) - %s', self.commit_file, e)

        return True

    """
    Commit changes with date.

    :param date: specific date to commit changes to. defaults to now
    """
    def commit(self, date=arrow.utcnow()):
        logger.info('Commiting > %s at %s', self.commit_file, date)
        index = self.repo.index
        index.add([self.commit_file])
        commit_time = date.format('YYYY-MM-DDTHH:mm:ss')
        index.commit("streaker strikes straight", author=self.author, committer=self.author, commit_date=commit_time, author_date=commit_time)



    """
    Check if the user hast write access the given path.
    If the path does not exist that it check the parent folder.
    This way the new repo could be initialized.

    :return: True if user has os.W_OK rights on the folder
    """
    def check_rights(self):
        # check full path
        if os.path.isdir(self.path):
            return os.access(self.path,os.W_OK)
        # check parent
        else:
            return os.access(os.path.dirname(self.path),os.W_OK)
