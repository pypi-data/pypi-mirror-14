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

define(["jquery","knockout","moment"],function(t,s,e){"use strict";function i(){this.calendar=function(){return""},this.toString=function(){return""}}function r(t,e){var r=!1;"string"==typeof t&&(t=parseInt(t)),"number"==typeof t&&(r=!0,t={id:t,url:"/api/commands/"+t+"/"}),this.raw=t,this.parent=e,this.id=t.id,this.downloadUrl=s.observable(),this.submitTime=s.observable(new i),this.startTime=s.observable(new i),this.finishTime=s.observable(new i),this.status=s.observable(),this.labelClass=s.observable(),this.hostTarget=s.observable(),this.command=s.observable(),this.stdout=s.observable(),this.stderr=s.observable(),r?this.reload():this._process(t)}function a(t){return t.length?e(t):new i}return r.constructor=r,r.prototype._process=function(t){switch(this.downloadUrl(t.zip_url),this.submitTime(a(t.submit_time)),this.startTime(a(t.start_time)),this.finishTime(a(t.finish_time)),this.status(t.status),this.hostTarget(t.host_target),this.command(t.command),this.stdout(t.std_out),this.stderr(t.std_err),t.status){case"finished":this.labelClass("label-success");break;case"running":this.labelClass("label-warning");break;case"pending":case"waiting":this.labelClass("label-info");break;default:this.labelClass("label-default")}},r.prototype.reload=function(){var s=this;return t.ajax({method:"GET",url:this.raw.url}).done(function(t){s.raw=t,s._process(t)})},r.prototype["delete"]=function(){t.ajax({method:"DELETE",url:this.raw.url})},r});