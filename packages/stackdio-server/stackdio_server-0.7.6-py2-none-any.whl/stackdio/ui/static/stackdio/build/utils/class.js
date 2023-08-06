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

define([],function(){var t=!1,n=/xyz/.test(function(){xyz})?/\b_super\b/:/.*/,e=function(){};return e.extend=function(e){function r(){!t&&this.init&&this.init.apply(this,arguments)}var i=this.prototype;t=!0;var u=new this;t=!1;for(var o in e)u[o]="function"==typeof e[o]&&"function"==typeof i[o]&&n.test(e[o])?function(t,n){return function(){var e=this._super;this._super=i[t];var r=n.apply(this,arguments);return this._super=e,r}}(o,e[o]):e[o];return r.prototype=u,r.prototype.constructor=r,r.extend=arguments.callee,r},e});