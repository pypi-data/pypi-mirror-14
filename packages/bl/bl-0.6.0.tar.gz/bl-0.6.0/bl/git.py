
import os
import git      # pip install GitPython

class Repo(git.Repo):
    """add some convenience methods to git.Repo"""

    def commit_all(self, msg, author=None):
        """commit the changes that have been made in the repository.
            msg = the commit message
            author = a git.util.Actor(name, email)
        """
        if self.is_dirty()!=True:
            return False
        else:
            changed_files = self.untracked_files \
                        + [diff.a_blob.path for diff in self.index.diff(None) 
                            if os.path.exists(diff.a_blob.abspath)]
            if len(changed_files) > 0:
                self.index.add(changed_files)

            deleted_files = [diff.a_blob.path for diff in self.index.diff(None) 
                                if not os.path.exists(diff.a_blob.abspath)]
            if len(deleted_files) > 0:
                self.index.remove(deleted_files)

            self.index.commit(msg, author=author)
