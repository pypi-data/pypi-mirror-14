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

define(["jquery","underscore","knockout","bootbox"],function(e,t,n,r){"use strict";function i(e,t){var r=!1;typeof e=="string"&&(e=parseInt(e)),typeof e=="number"&&(r=!0,e={id:e,url:"/api/stacks/"+e+"/hosts/"}),this.raw=e,this.parent=t,this.id=e.id,this.hostname=n.observable(),this.fqdn=n.observable(),this.publicDNS=n.observable(),this.privateDNS=n.observable(),this.hostDefinition=n.observable(),this.status=n.observable(),this.state=n.observable(),this.labelClass=n.observable(),r?this.reload():this._process(e)}return i.constructor=i,i.prototype._process=function(e){this.hostname(e.hostname),this.fqdn(e.fqdn),this.publicDNS(e.provider_dns),this.privateDNS(e.provider_private_dns),this.hostDefinition(e.blueprint_host_definition),this.status(e.status),this.state(e.state);switch(e.state){case"running":this.labelClass("label-success");break;case"shutting-down":case"stopping":case"launching":case"deleting":this.labelClass("label-warning");break;case"terminated":case"stopped":this.labelClass("label-danger");break;case"pending":this.labelClass("label-info");break;default:this.labelClass("label-default")}},i.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},i.prototype.delete=function(){var t=this;r.confirm({title:"Confirm delete of <strong>"+stackTitle+"</strong>",message:"Are you sure you want to delete <strong>"+stackTitle+"</strong>?<br>"+"This will terminate all infrastructure, in addition to "+"removing all history related to this stack.",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(n){n&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(e){t.raw=e,t._process(e)}).fail(function(e){var t;try{var n=JSON.parse(e.responseText);t=n.detail.join("<br>")}catch(i){t="Oops... there was a server error.  This has been reported to your administrators."}r.alert({title:"Error deleting stack",message:t})})}})},i});