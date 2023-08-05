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

define(["jquery","knockout","bootbox","utils/utils","models/host-definition"],function(e,t,n,r,i){"use strict";function s(e,n){var r=!1;typeof e=="string"&&(e=parseInt(e)),typeof e=="number"&&(r=!0,e={id:e,url:"/api/cloud/snapshots/"+e+"/"}),this.raw=e,this.parent=n,this.id=e.id,this.title=t.observable(),this.description=t.observable(),this.accountId=t.observable(),this.snapshotId=t.observable(),this.sizeInGB=t.observable(),this.filesystemType=t.observable(),r?this.waiting=this.reload():this._process(e)}return s.constructor=s,s.prototype._process=function(e){this.title(e.title),this.description(e.description),this.accountId(e.account),this.snapshotId(e.snapshot_id),this.sizeInGB(e.size_in_gb),this.filesystemType(e.filesystem_type)},s.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},s.prototype.save=function(){var t=this,n=["title","description","snapshot_id","size_in_gb","filesystem_type"];n.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()}),e.ajax({method:"PUT",url:t.raw.url,data:JSON.stringify({title:t.title(),description:t.description(),snapshot_id:t.snapshotId(),size_in_gb:t.sizeInGB(),filesystem_type:t.filesystemType()})}).done(function(e){r.growlAlert("Successfully saved snapshot!","success");try{t.parent.snapshotTitle(e.title)}catch(n){}}).fail(function(e){r.parseSaveError(e,"snapshot",n)})},s.prototype.delete=function(){var t=this,r=this.title();n.confirm({title:"Confirm delete of <strong>"+r+"</strong>",message:"Are you sure you want to delete <strong>"+r+"</strong>?",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(r){r&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(){window.location.pathname!=="/snapshots/"?window.location="/snapshots/":t.parent&&typeof t.parent.reload=="function"&&t.parent.reload()}).fail(function(e){var t;try{var r=JSON.parse(e.responseText);t=r.detail.join("<br>")}catch(i){t="Oops... there was a server error.  This has been reported to your administrators."}n.alert({title:"Error deleting snapshot",message:t})})}})},s});