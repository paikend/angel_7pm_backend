#! /usr/bin/env bash
git add -f env/etc
eb deploy --staged
git reset HEAD env/etc