## process
### setup
- [poetry](https://python-poetry.org/docs/basic-usage/)
```sh
poetry new poetry-demo
cd poetry-demo
poetry init
```
- [create bucket](https://docs.aws.amazon.com/cli/latest/reference/s3/mb.html)
	- `aws s3 mb s3://mybucket`
- secrets mgmt setup
```sh
conda activate smgmt
python -m pip install --editable .
smgmt --help
```

### run api
https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry
```sh
poetry run start
```

### install extension
- go to `chrome://extensions/`
- click "Load unpacked" and select extension folder

### check records
- `aws s3 ls s3://knowledgeproject/dev/test/`


## tracking api
- find and replace instances of `test01_api`
- setup new config file with secrets manager
```sh
smgmt create -n tracking-api -s '{"aws_bucket":"<bucket>","object_prefix":"dev/tracking-api"}' --config
```
