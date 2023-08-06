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

define(["jquery","knockout","bootbox","utils/utils","models/host-definition"],function(t,e,s,o,i){"use strict";function r(t,s){var o=!1;"string"==typeof t&&(t=parseInt(t)),"number"==typeof t&&(o=!0,t={id:t,url:"/api/cloud/snapshots/"+t+"/"}),this.raw=t,this.parent=s,this.id=t.id,this.title=e.observable(),this.description=e.observable(),this.accountId=e.observable(),this.snapshotId=e.observable(),this.sizeInGB=e.observable(),this.filesystemType=e.observable(),o?this.waiting=this.reload():this._process(t)}return r.constructor=r,r.prototype._process=function(t){this.title(t.title),this.description(t.description),this.accountId(t.account),this.snapshotId(t.snapshot_id),this.sizeInGB(t.size_in_gb),this.filesystemType(t.filesystem_type)},r.prototype.reload=function(){var e=this;return t.ajax({method:"GET",url:this.raw.url}).done(function(t){e.raw=t,e._process(t)})},r.prototype.save=function(){var e=this,s=["title","description","snapshot_id","size_in_gb","filesystem_type"];s.forEach(function(e){var s=t("#"+e);s.removeClass("has-error");var o=s.find(".help-block");o.remove()}),t.ajax({method:"PUT",url:e.raw.url,data:JSON.stringify({title:e.title(),description:e.description(),snapshot_id:e.snapshotId(),size_in_gb:e.sizeInGB(),filesystem_type:e.filesystemType()})}).done(function(t){o.growlAlert("Successfully saved snapshot!","success");try{e.parent.snapshotTitle(t.title)}catch(s){}}).fail(function(t){o.parseSaveError(t,"snapshot",s)})},r.prototype["delete"]=function(){var e=this,o=this.title();s.confirm({title:"Confirm delete of <strong>"+o+"</strong>",message:"Are you sure you want to delete <strong>"+o+"</strong>?",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(o){o&&t.ajax({method:"DELETE",url:e.raw.url}).done(function(){"/snapshots/"!==window.location.pathname?window.location="/snapshots/":e.parent&&"function"==typeof e.parent.reload&&e.parent.reload()}).fail(function(t){var e;try{var o=JSON.parse(t.responseText);e=o.detail.join("<br>")}catch(i){e="Oops... there was a server error.  This has been reported to your administrators."}s.alert({title:"Error deleting snapshot",message:e})})}})},r});