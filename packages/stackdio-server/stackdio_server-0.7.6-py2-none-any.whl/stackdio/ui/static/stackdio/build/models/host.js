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

define(["jquery","underscore","knockout","bootbox"],function(t,e,s,a){"use strict";function r(t,e){var a=!1;"string"==typeof t&&(t=parseInt(t)),"number"==typeof t&&(a=!0,t={id:t,url:"/api/stacks/"+t+"/hosts/"}),this.raw=t,this.parent=e,this.id=t.id,this.hostname=s.observable(),this.fqdn=s.observable(),this.publicDNS=s.observable(),this.privateDNS=s.observable(),this.hostDefinition=s.observable(),this.status=s.observable(),this.state=s.observable(),this.labelClass=s.observable(),a?this.reload():this._process(t)}return r.constructor=r,r.prototype._process=function(t){switch(this.hostname(t.hostname),this.fqdn(t.fqdn),this.publicDNS(t.provider_dns),this.privateDNS(t.provider_private_dns),this.hostDefinition(t.blueprint_host_definition),this.status(t.status),this.state(t.state),t.state){case"running":this.labelClass("label-success");break;case"shutting-down":case"stopping":case"launching":case"deleting":this.labelClass("label-warning");break;case"terminated":case"stopped":this.labelClass("label-danger");break;case"pending":this.labelClass("label-info");break;default:this.labelClass("label-default")}},r.prototype.reload=function(){var e=this;return t.ajax({method:"GET",url:this.raw.url}).done(function(t){e.raw=t,e._process(t)})},r.prototype["delete"]=function(){var e=this;a.confirm({title:"Confirm delete of <strong>"+stackTitle+"</strong>",message:"Are you sure you want to delete <strong>"+stackTitle+"</strong>?<br>This will terminate all infrastructure, in addition to removing all history related to this stack.",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(s){s&&t.ajax({method:"DELETE",url:e.raw.url}).done(function(t){e.raw=t,e._process(t)}).fail(function(t){var e;try{var s=JSON.parse(t.responseText);e=s.detail.join("<br>")}catch(r){e="Oops... there was a server error.  This has been reported to your administrators."}a.alert({title:"Error deleting stack",message:e})})}})},r});