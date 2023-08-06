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

define(["knockout","models/formula-component","models/access-rule","models/blueprint-volume"],function(e,s,t,o){"use strict";function i(s,t){var o=!1;"string"==typeof s&&(s=parseInt(s)),"number"==typeof s&&(o=!0,s={id:s,url:"/api/stacks/"+s+"/hosts/"}),this.raw=s,this.id=s.id,this.parent=t,this.title=e.observable(),this.description=e.observable(),this.cloudImage=e.observable(),this.count=e.observable(),this.hostnameTemplate=e.observable(),this.size=e.observable(),this.spotPrice=e.observable(),this.zone=e.observable(),this.subnetId=e.observable(),this.components=e.observableArray([]),this.accessRules=e.observableArray([]),this.volumes=e.observableArray([]),o?this.reload():this._process(s)}return i.constructor=i,i.prototype._process=function(e){this.title(e.title),this.description(e.description),this.cloudImage(e.cloud_image),this.count(e.count),this.hostnameTemplate(e.hostname_template),this.size(e.size),this.zone(e.zone),this.subnetId(e.subnetId),this.spotPrice(e.spot_price);var i=this;this.components(e.formula_components.map(function(e){return new s(e,i.parent,i)})),this.accessRules(e.access_rules.map(function(e){return new t(e,i.parent,i)})),this.volumes(e.volumes.map(function(e){return new o(e,i.parent,i)}))},i});