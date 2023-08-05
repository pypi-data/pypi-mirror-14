Issues and Bugs
===============
If you have a bug report or idea for improvement, please create an issue on GitHub, or a pull request with the fix.

Contributors
============

Pull Request Checklist
----------------------

1. Verify tests pass:
  ::

      tox

2. If you have PyCharm, use it to see if your changes introduce any new static analysis warnings.

3. Modify CHANGELOG.rst to say what you changed.

Maintainers
===========

Review Checklist
----------------
On every pull request:

1. Verify changes are sensible and in line with project goals.
2. Verify tests pass (continuous integration is OK for this).
3. Use PyCharm to check static analysis if changes are significant or non-trivial.
4. Verify CHANGELOG.rst is modified as appropriate.
5. Merge in.


Release Checklist
-----------------

1. Verify tests pass.

2. Use check-manifest_ to verify that no files are missing:
  ::

      check-manifest

3. Use :code:`git status` to verify that no superfluous files are present to be included in the source distribution.

4. Increment version number from last release according to PEP 0440 and roughly according to the Semantic Versioning guidelines.

5. Modify CHANGELOG file to reflect new version number.

6. Build distributions:
  ::

      python setup.py sdist bdist_wheel

7. Visually inspect source distribution for correctness.

8. Upload to testpypi if changes impact PyPI (e.g., if README changed):
  ::

      twine upload -r test  dist\ezoutlet-x.y.z-py2-none-any.whl dist\ezoutlet-0.0.1-dev3.zip


9. Upload to pypi:
  ::

      twine upload dist\ezoutlet-x.y.z-py2-none-any.whl dist\ezoutlet-0.0.1-dev3.zip

.. _check-manifest: https://pypi.python.org/pypi/check-manifest

10. Create accompanying release on GitHub.
