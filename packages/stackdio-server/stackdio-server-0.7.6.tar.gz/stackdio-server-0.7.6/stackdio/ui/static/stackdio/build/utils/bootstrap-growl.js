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

!function(t,e){"object"==typeof exports?module.exports=e(require("jquery","bootstrap")):"function"==typeof define&&define.amd&&define(["jquery","bootstrap"],e)}(this,function(t){t.bootstrapGrowl=function(e,o){var a,i,s;o=t.extend({},t.bootstrapGrowl.default_options,o),a=t("<div>"),a.attr("class","bootstrap-growl alert"),o.type&&a.addClass("alert-"+o.type),o.allow_dismiss&&a.append('<a class="close" data-dismiss="alert" href="#">&times;</a>'),a.append(e);var d=t(window).width()<=767;return s=d?63:-10,t(".bootstrap-growl").each(function(){return s=Math.max(s,parseInt(t(this).css("top"))+t(this).outerHeight()+o.stackup_spacing)}),i={position:d?"fixed":"absolute",margin:"0","z-index":9999,display:"none",width:o.width,"max-width":t(window).width()-50,top:s+"px",right:"25px"},a.css(i),t(o.ele).append(a),a.fadeIn(),o.delay>0?a.delay(o.delay).fadeOut(function(){return t(this).remove()}):void 0},t.bootstrapGrowl.default_options={ele:"body",type:null,align:"right",width:"100%",delay:4e3,allow_dismiss:!0,stackup_spacing:10}});