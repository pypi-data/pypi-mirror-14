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

define(["jquery","knockout","bootbox","utils/utils"],function(e,t,i,s){"use strict";function r(e,i){var s=!1;"string"==typeof e&&(e=parseInt(e)),"number"==typeof e&&(s=!0,e={id:e,url:"/api/cloud/images/"+e+"/"}),this.raw=e,this.parent=i,this.id=e.id,this.title=t.observable(),this.description=t.observable(),this.slug=t.observable(),this.imageId=t.observable(),this.defaultInstanceSize=t.observable(),this.sshUser=t.observable(),s?this.waiting=this.reload():this._process(e)}return r.constructor=r,r.prototype._process=function(e){this.title(e.title),this.description(e.description),this.slug(e.slug),this.imageId(e.image_id),this.defaultInstanceSize(e.default_instance_size),this.sshUser(e.ssh_user)},r.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},r.prototype.save=function(){var t=this,i=["title","description","image_id","default_instance_size","ssh_user"];i.forEach(function(t){var i=e("#"+t);i.removeClass("has-error");var s=i.find(".help-block");s.remove()}),e.ajax({method:"PUT",url:t.raw.url,data:JSON.stringify({title:t.title(),description:t.description(),image_id:t.imageId(),default_instance_size:t.defaultInstanceSize(),ssh_user:t.sshUser()})}).done(function(e){s.growlAlert("Successfully saved cloud image!","success");try{t.parent.imageTitle(e.title)}catch(i){}}).fail(function(e){s.parseSaveError(e,"cloud image",i)})},r.prototype["delete"]=function(){var t=this,s=this.title();i.confirm({title:"Confirm delete of <strong>"+s+"</strong>",message:"Are you sure you want to delete <strong>"+s+"</strong>?",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(s){s&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(){"/images/"!==window.location.pathname?window.location="/images/":t.parent&&"function"==typeof t.parent.reload&&t.parent.reload()}).fail(function(e){var t;try{var s=JSON.parse(e.responseText);t=s.detail.join("<br>"),Object.keys(s).indexOf("blueprints")>=0&&(t+="<br><br>Blueprints:<ul><li>"+s.blueprints.join("</li><li>")+"</li></ul>")}catch(r){t="Oops... there was a server error.  This has been reported to your administrators."}i.alert({title:"Error deleting cloud image",message:t})})}})},r});