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

define(["jquery","knockout","utils/utils","generics/pagination","models/label"],function(e,a,l,r,t){"use strict";return r.extend({parentModel:null,parentId:null,parentObject:a.observable(),newLabels:a.observableArray([]),newLabelKey:a.observable(),autoRefresh:!1,model:t,sortableFields:[{name:"key",displayName:"Key",width:"45%"},{name:"value",displayName:"Value",width:"45%"}],init:function(){this._super(),this.newLabelKey(null),this.parentObject(new this.parentModel(this.parentId,this))},addNewLabel:function(){var r=e("#new-label-form");r.removeClass("has-error");var t=this,n=!1;return this.sortedObjects().forEach(function(e){e.key()===t.newLabelKey()&&(n=!0)}),this.newLabels().forEach(function(e){e.key===t.newLabelKey()&&(n=!0)}),n?(l.growlAlert("You may not have two labels with the same key.","danger"),void r.addClass("has-error")):(this.newLabels.push({key:this.newLabelKey(),value:a.observable(null)}),void this.newLabelKey(null))},deleteNewLabel:function(e){this.newLabels.remove(e)},saveLabels:function(){var a=[],r=this;this.objects().forEach(function(t){var n=t.value();a.push(e.ajax({method:"PUT",url:r.parentObject().raw.labels+t.key()+"/",data:JSON.stringify({value:n?n:null})}).fail(function(e){404!==e.status&&l.alertError(e,"Error saving label","Errors saving label for "+t.key()+":<br>")}))}),this.newLabels().forEach(function(t){var n=t.value();a.push(e.ajax({method:"POST",url:r.parentObject().raw.labels,data:JSON.stringify({key:t.key,value:n?n:null})}).fail(function(e){l.alertError(e,"Error saving label","Errors saving label for "+t.key+":<br>")}))}),e.when.apply(this,a).done(function(){l.growlAlert("Successfully saved labels!","success"),r.newLabels([]),r.reload()})}})});