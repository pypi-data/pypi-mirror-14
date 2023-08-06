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

define(["jquery","select2"],function(e){"use strict";return{getAllFormulas:function(t){function n(a){e.ajax({method:"GET",url:a}).done(function(e){r.push.apply(r,e.results),null===e.next?t(r):n(e.next)})}var r=[];n("/api/formulas/")},createVersionSelector:function(t,n){for(var r=null,a=0,o=n.length;o>a;++a)if(n[a].uri===t.formula()){r=n[a].valid_versions;break}if(!r)return!1;var u=e("#"+t.formulaHtmlId()),l=t.version();return u.append('<option value="'+l+'" title="'+l+'">'+l+"</option>"),u.removeClass("hidden-formula-versions"),u.select2({ajax:{url:r,dataType:"json",delay:100,data:function(e){return{title:e.term}},processResults:function(e){var t=[];return e.results.forEach(function(e){t.push({id:e,text:e,version:e})}),{results:t}},cache:!0},theme:"bootstrap",placeholder:"Select a version...",templateResult:function(e){return e.text},minimumInputLength:0}),u.val(l).trigger("change"),u.on("select2:select",function(e){var n=e.params.data;t.version(n.version)}),!0}}});