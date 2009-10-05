#!/bin/bash

# Install two Ruby gems:
#   - 4store-ruby
#   - rqommend

GEMS_PATH=http://moustaki.org/gems/

wget ${GEMS_PATH}4store-ruby.gem
wget ${GEMS_PATH}rqommend.gem

gem install 4store-ruby.gem
gem install rqommend.gem

