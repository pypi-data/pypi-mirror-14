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

define(["knockout"],function(r){"use strict";function e(e,o){this.raw=e,this.parent=o,this.formula=r.observable(),this.version=r.observable(),this.formulaHtmlId=r.observable(),this._process(e)}return e.constructor=e,e.prototype._process=function(r){this.formula(r.formula),this.version(r.version),this.formulaHtmlId(r.formula.replace(/\//g,"-").replace(/:/g,"-").replace(/\./g,"-").replace(/@/g,"-"))},e});