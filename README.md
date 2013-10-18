<!-- Licensed under the Apache License. See footer for details. -->

cf-buildpack-nodejs
================================================================================

An alterative buildpack for [Node.js](http://nodejs.org/), 
for [CloudFoundry](http://cloudfoundry.com/).

usage
--------------------------------------------------------------------------------

in your `manifest.yml` file, you should add an entry for `nodejs-version`, so
your manifest may look like this:

    ---
    nodejs-version: v0.10.20
    applications:
    - name:      my-app
      command:   node my-app.js    
      buildpack: https://github.com/pmuellr/cf-buildpack-nodejs.git

The value for `nodejs-version` should be one of the versioned directories
relative to <http://nodejs.org/dist/>.

<!--
#===============================================================================
# Copyright 2013 Patrick Mueller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================
-->