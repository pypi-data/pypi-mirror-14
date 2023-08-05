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

define(["jquery","knockout","moment"],function(e,t,n){"use strict";function r(){this.calendar=function(){return""},this.toString=function(){return""}}function i(e,n){var i=!1;typeof e=="string"&&(e=parseInt(e)),typeof e=="number"&&(i=!0,e={id:e,url:"/api/commands/"+e+"/"}),this.raw=e,this.parent=n,this.id=e.id,this.downloadUrl=t.observable(),this.submitTime=t.observable(new r),this.startTime=t.observable(new r),this.finishTime=t.observable(new r),this.status=t.observable(),this.labelClass=t.observable(),this.hostTarget=t.observable(),this.command=t.observable(),this.stdout=t.observable(),this.stderr=t.observable(),i?this.reload():this._process(e)}function s(e){return e.length?n(e):new r}return i.constructor=i,i.prototype._process=function(e){this.downloadUrl(e.zip_url),this.submitTime(s(e.submit_time)),this.startTime(s(e.start_time)),this.finishTime(s(e.finish_time)),this.status(e.status),this.hostTarget(e.host_target),this.command(e.command),this.stdout(e.std_out),this.stderr(e.std_err);switch(e.status){case"finished":this.labelClass("label-success");break;case"running":this.labelClass("label-warning");break;case"pending":case"waiting":this.labelClass("label-info");break;default:this.labelClass("label-default")}},i.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},i.prototype.delete=function(){e.ajax({method:"DELETE",url:this.raw.url})},i});