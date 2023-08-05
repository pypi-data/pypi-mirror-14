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

define(["knockout","models/formula-component","models/access-rule","models/blueprint-volume"],function(e,t,n,r){"use strict";function i(t,n){var r=!1;typeof t=="string"&&(t=parseInt(t)),typeof t=="number"&&(r=!0,t={id:t,url:"/api/stacks/"+t+"/hosts/"}),this.raw=t,this.id=t.id,this.parent=n,this.title=e.observable(),this.description=e.observable(),this.cloudImage=e.observable(),this.count=e.observable(),this.hostnameTemplate=e.observable(),this.size=e.observable(),this.spotPrice=e.observable(),this.zone=e.observable(),this.subnetId=e.observable(),this.components=e.observableArray([]),this.accessRules=e.observableArray([]),this.volumes=e.observableArray([]),r?this.reload():this._process(t)}return i.constructor=i,i.prototype._process=function(e){this.title(e.title),this.description(e.description),this.cloudImage(e.cloud_image),this.count(e.count),this.hostnameTemplate(e.hostname_template),this.size(e.size),this.zone(e.zone),this.subnetId(e.subnetId),this.spotPrice(e.spot_price);var i=this;this.components(e.formula_components.map(function(e){return new t(e,i.parent,i)})),this.accessRules(e.access_rules.map(function(e){return new n(e,i.parent,i)})),this.volumes(e.volumes.map(function(e){return new r(e,i.parent,i)}))},i});