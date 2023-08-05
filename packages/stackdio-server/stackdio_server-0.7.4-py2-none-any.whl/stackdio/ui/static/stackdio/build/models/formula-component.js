/*!
  * Copyright 2014,  Digital Reasoning
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *     http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
*/

define(["knockout"],function(e){"use strict";function t(t,n,r){this.raw=t,this.parent=n,this.hostDefinition=r,this.formula=e.observable(),this.title=e.observable(),this.description=e.observable(),this.slsPath=e.observable(),this.order=e.observable(),this._process(t)}return t.constructor=t,t.prototype._process=function(e){this.formula(e.formula),this.title(e.title),this.description(e.description),this.slsPath(e.sls_path),this.order(e.order)},t});