#!/bin/bash -eux

# rationale: This make a tag to remote repo and push this
# create a secret with travis CI command
# travis login && travis token # AdminSwissTierrasColombia
# travis encrypt GH_TOKEN_ASISTENTE_LADM_COL_DOCS="$GH_TOKEN_ASISTENTE_LADM_COL_DOCS"
# link: https://github.com/travis-ci/travis.rb#installation
REMOTE_REPO_SLUG="$REMOTE_REPO_OWNER/$REMOTE_REPO_NAME"

clone_repo() {
  rm -rf ${REMOTE_REPO_NAME} # repo never exists in travis
  git clone -b master --depth 10 https://github.com/${REMOTE_REPO_SLUG}
  pushd ${REMOTE_REPO_NAME}
  # GH_ADMINAGENCIAIMPL_ACCESS_TOKEN is stablished in .travis.yml as a secret
  git remote add origin-token https://${GH_TOKEN_ASISTENTE_LADM_COL_DOCS}@github.com/${REMOTE_REPO_SLUG}.git > /dev/null 2>&1
  popd
}

install_deps() {
  pushd ${REMOTE_REPO_NAME}
  cat packages.txt | xargs sudo apt-get install
  pip install -r requirements.txt
  popd
}

# link: https://docs.travis-ci.com/user/environment-variables/
# link: https://en.wikipedia.org/wiki/Language_code
build_repo() {
  pushd ${REMOTE_REPO_NAME}
  ./generate.sh
  mkdir "$TRAVIS_BUILD_DIR/asistente_ladm_col/help"
  # all available languages
  for lang_path in $(ls -d src/build/*)
  do
    lang=$(basename $lang_path)
    cp -r "$lang_path/html/master" "$TRAVIS_BUILD_DIR/asistente_ladm_col/help/$lang"
  done
  popd
}

push_tag() {
  pushd ${REMOTE_REPO_NAME}
  git commit --allow-empty -m "Release version $TRAVIS_TAG of Asistente-LADM_COL" -m 'Commited from https://github.com/SwissTierrasColombia/Asistente-LADM_COL'
  git tag "$TRAVIS_TAG"
  git push origin-token master # the release branch to be commited
  git push origin-token "$TRAVIS_TAG"
  popd
}

clone_repo
#install_deps
#build_repo
push_tag
