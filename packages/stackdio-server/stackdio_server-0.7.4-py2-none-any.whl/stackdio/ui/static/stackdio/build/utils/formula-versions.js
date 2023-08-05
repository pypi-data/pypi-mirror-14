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

define(["jquery","select2"],function(e){"use strict";return{getAllFormulas:function(t){function r(i){e.ajax({method:"GET",url:i}).done(function(e){n.push.apply(n,e.results),e.next===null?t(n):r(e.next)})}var n=[];r("/api/formulas/")},createVersionSelector:function(t,n){var r=null;for(var i=0,s=n.length;i<s;++i)if(n[i].uri===t.formula()){r=n[i].valid_versions;break}if(!r)return!1;var o=e("#"+t.formulaHtmlId()),u=t.version();return o.append('<option value="'+u+'" title="'+u+'">'+u+"</option>"),o.removeClass("hidden-formula-versions"),o.select2({ajax:{url:r,dataType:"json",delay:100,data:function(e){return{title:e.term}},processResults:function(e){var t=[];return e.results.forEach(function(e){t.push({id:e,text:e,version:e})}),{results:t}},cache:!0},theme:"bootstrap",placeholder:"Select a version...",templateResult:function(e){return e.text},minimumInputLength:0}),o.val(u).trigger("change"),o.on("select2:select",function(e){var n=e.params.data;t.version(n.version)}),!0}}});