#!/usr/bin/env bash

set -euxo pipefail

stylus *.styl
civet < index.civet > index.js
pug *.pug
