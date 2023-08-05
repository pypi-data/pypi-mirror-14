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

define(["jquery","knockout","bootbox","utils/utils"],function(e,t,n,r){"use strict";function i(e,n){var r=!1;typeof e=="string"&&(e=parseInt(e)),typeof e=="number"&&(r=!0,e={id:e,url:"/api/cloud/images/"+e+"/"}),this.raw=e,this.parent=n,this.id=e.id,this.title=t.observable(),this.description=t.observable(),this.slug=t.observable(),this.imageId=t.observable(),this.defaultInstanceSize=t.observable(),this.sshUser=t.observable(),r?this.waiting=this.reload():this._process(e)}return i.constructor=i,i.prototype._process=function(e){this.title(e.title),this.description(e.description),this.slug(e.slug),this.imageId(e.image_id),this.defaultInstanceSize(e.default_instance_size),this.sshUser(e.ssh_user)},i.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},i.prototype.save=function(){var t=this,n=["title","description","image_id","default_instance_size","ssh_user"];n.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()}),e.ajax({method:"PUT",url:t.raw.url,data:JSON.stringify({title:t.title(),description:t.description(),image_id:t.imageId(),default_instance_size:t.defaultInstanceSize(),ssh_user:t.sshUser()})}).done(function(e){r.growlAlert("Successfully saved cloud image!","success");try{t.parent.imageTitle(e.title)}catch(n){}}).fail(function(e){r.parseSaveError(e,"cloud image",n)})},i.prototype.delete=function(){var t=this,r=this.title();n.confirm({title:"Confirm delete of <strong>"+r+"</strong>",message:"Are you sure you want to delete <strong>"+r+"</strong>?",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(r){r&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(){window.location.pathname!=="/images/"?window.location="/images/":t.parent&&typeof t.parent.reload=="function"&&t.parent.reload()}).fail(function(e){var t;try{var r=JSON.parse(e.responseText);t=r.detail.join("<br>"),Object.keys(r).indexOf("blueprints")>=0&&(t+="<br><br>Blueprints:<ul><li>"+r.blueprints.join("</li><li>")+"</li></ul>")}catch(i){t="Oops... there was a server error.  This has been reported to your administrators."}n.alert({title:"Error deleting cloud image",message:t})})}})},i});