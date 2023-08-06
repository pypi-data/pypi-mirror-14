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

define(["knockout"],function(t){"use strict";function o(o,r,s){this.raw=o,this.parent=r,this.hostDefinition=s,this.rule=t.observable(),this.fromPort=t.observable(),this.toPort=t.observable(),this._process(o)}return o.constructor=o,o.prototype._process=function(t){this.rule(t.rule),this.fromPort(t.from_port),this.toPort(t.to_port)},o});