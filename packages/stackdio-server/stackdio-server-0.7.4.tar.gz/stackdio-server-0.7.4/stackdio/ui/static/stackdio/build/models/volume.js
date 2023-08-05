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

define(["jquery","knockout"],function(e,t){"use strict";function n(e,n){var r=!1;typeof e=="string"&&(e=parseInt(e)),typeof e=="number"&&(r=!0,e={id:e,url:"/api/volumes/"+e+"/"}),this.raw=e,this.parent=n,this.id=e.id,this.volumeId=t.observable(),this.attachTime=t.observable(),this.hostname=t.observable(),this.snapshotName=t.observable(),this.size=t.observable(),this.device=t.observable(),this.mountPoint=t.observable(),r?this.reload():this._process(e)}return n.constructor=n,n.prototype._process=function(e){this.volumeId(e.volume_id),this.attachTime(e.attach_time),this.hostname(e.hostname),this.snapshotName(e.snapshot_name),this.size(e.size_in_gb),this.device(e.device),this.mountPoint(e.mount_point)},n.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},n});