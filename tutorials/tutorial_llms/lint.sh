(IMAGE=623860924167.dkr.ecr.eu-north-1.amazonaws.com/dev_tools:prod \
        docker-compose \
        --file lint-docker-compose.yml \
        --env-file default.env \
        run \
        --rm \
        --name saggese.cmamp.linter.cmamp1.20240725_212432 \
        --user $(id -u):$(id -g) \
        linter \
        pre-commit run -c /app/.pre-commit-config.yaml --files $* ) 2>&1 | tee -a linter_output.txt
