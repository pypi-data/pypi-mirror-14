/*!
  * Copyright 2016,  Digital Reasoning
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

define(["knockout"],function(t){"use strict";function s(s,i,e){this.raw=s,this.parent=i,this.hostDefinition=e,this.formula=t.observable(),this.title=t.observable(),this.description=t.observable(),this.slsPath=t.observable(),this.order=t.observable(),this._process(s)}return s.constructor=s,s.prototype._process=function(t){this.formula(t.formula),this.title(t.title),this.description(t.description),this.slsPath(t.sls_path),this.order(t.order)},s});