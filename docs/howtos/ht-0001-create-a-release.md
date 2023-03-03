# How to create and deploy a release

1. Run the style checks and tests to ensure everything is pretty and working
   ```shell
   make checks tests
   ```

2. Update the Changelog
   ```shell
   git add CHANGELOG.rst
   git commit
   ```

3. Update the release number and push the repository
   ```shell
   bumpver update
   ```
