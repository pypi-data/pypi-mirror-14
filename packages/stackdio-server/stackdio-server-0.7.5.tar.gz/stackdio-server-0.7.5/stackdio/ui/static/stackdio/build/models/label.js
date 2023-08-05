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

define(["knockout","bootbox","underscore"],function(e,t,n){"use strict";function r(t,n){this.raw=t,this.parent=n,this.key=e.observable(),this.value=e.observable(),this._process(t)}return r.constructor=r,r.prototype._process=function(e){this.key(e.key),this.value(e.value)},r.prototype.delete=function(){var e=this,r=n.escape(e.key());t.confirm({title:"Confirm delete of <strong>"+r+"</strong>",message:"Are you sure you want to delete the label <strong>"+r+"</strong>?",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(n){n&&$.ajax({method:"DELETE",url:e.raw.url}).done(function(){e.parent.reload&&e.parent.reload()}).fail(function(e){var n;try{var r=JSON.parse(e.responseText);n=r.detail.join("<br>")}catch(i){n="Oops... there was a server error.  This has been reported to your administrators."}t.alert({title:"Error deleting label",message:n})})}})},r});