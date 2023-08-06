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

!function(t,e){"use strict";function a(){if("standalone"in t.navigator&&t.navigator.standalone){var a="a";$("body").delegate(a,"click",function(t){if($(this).attr("target")==e||""==$(this).attr("target")||"_self"==$(this).attr("target")){var a=$(this).attr("href");a.match(/^http(s?)/g)||(t.preventDefault(),self.location=a)}})}}"function"==typeof require?require(["jquery"],function(t){t(document).ready(a)}):$(document).ready(a)}(window);