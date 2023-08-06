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

define(["jquery","knockout"],function(t,e){"use strict";function s(t,s){var i=!1;"string"==typeof t&&(t=parseInt(t)),"number"==typeof t&&(i=!0,t={id:t,url:"/api/volumes/"+t+"/"}),this.raw=t,this.parent=s,this.id=t.id,this.volumeId=e.observable(),this.attachTime=e.observable(),this.hostname=e.observable(),this.snapshotName=e.observable(),this.size=e.observable(),this.device=e.observable(),this.mountPoint=e.observable(),i?this.reload():this._process(t)}return s.constructor=s,s.prototype._process=function(t){this.volumeId(t.volume_id),this.attachTime(t.attach_time),this.hostname(t.hostname),this.snapshotName(t.snapshot_name),this.size(t.size_in_gb),this.device(t.device),this.mountPoint(t.mount_point)},s.prototype.reload=function(){var e=this;return t.ajax({method:"GET",url:this.raw.url}).done(function(t){e.raw=t,e._process(t)})},s});