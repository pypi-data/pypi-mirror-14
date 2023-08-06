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

define(["jquery","knockout","bootbox"],function(e,t,r){"use strict";function o(e,r){var o=!1;"string"==typeof e&&(e=parseInt(e)),"number"==typeof e&&(o=!0,e={id:e,url:"/api/commands/"+e+"/"}),this.raw=e,this.parent=r,this.id=e.id,this.name=t.observable(),this.description=t.observable(),this.groupId=t.observable(),this["default"]=t.observable(),this.managed=t.observable(),o?this.reload():this._process(e)}return o.constructor=o,o.prototype._process=function(e){this.name(e.name),this.description(e.description),this.groupId(e.group_id),this["default"](e["default"]),this.managed(e.managed)},o.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},o.prototype["delete"]=function(){var t=this,o=this.name(),s="Are you sure you want to delete <strong>"+o+"</strong>?";s+=this.managed()?"<br>This <strong>will</strong> delete the group from the provider in addition to locally.":"<br>This will <strong>not</strong> delete the group on the provider, it will only delete stackd.io's record of it.",r.confirm({title:"Confirm delete of <strong>"+o+"</strong>",message:s,buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(o){o&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(){t.parent.reload&&t.parent.reload()}).fail(function(e){var t;try{var o=JSON.parse(e.responseText);t=o.detail.join("<br>")}catch(s){t="Oops... there was a server error.  This has been reported to your administrators."}r.alert({title:"Error deleting security group",message:t})})}})},o});