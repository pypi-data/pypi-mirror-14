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

define(["jquery","knockout","utils/utils","generics/pagination","models/label"],function(e,t,n,r,i){"use strict";return r.extend({parentModel:null,parentId:null,parentObject:t.observable(),newLabels:t.observableArray([]),newLabelKey:t.observable(),autoRefresh:!1,model:i,sortableFields:[{name:"key",displayName:"Key",width:"45%"},{name:"value",displayName:"Value",width:"45%"}],init:function(){this._super(),this.newLabelKey(null),this.parentObject(new this.parentModel(this.parentId,this))},addNewLabel:function(){var r=e("#new-label-form");r.removeClass("has-error");var i=this,s=!1;this.sortedObjects().forEach(function(e){e.key()===i.newLabelKey()&&(s=!0)}),this.newLabels().forEach(function(e){e.key===i.newLabelKey()&&(s=!0)});if(s){n.growlAlert("You may not have two labels with the same key.","danger"),r.addClass("has-error");return}this.newLabels.push({key:this.newLabelKey(),value:t.observable(null)}),this.newLabelKey(null)},deleteNewLabel:function(e){this.newLabels.remove(e)},saveLabels:function(){var t=[],r=this;this.objects().forEach(function(i){var s=i.value();t.push(e.ajax({method:"PUT",url:r.parentObject().raw.labels+i.key()+"/",data:JSON.stringify({value:s?s:null})}).fail(function(e){e.status!==404&&n.alertError(e,"Error saving label","Errors saving label for "+i.key()+":<br>")}))}),this.newLabels().forEach(function(i){var s=i.value();t.push(e.ajax({method:"POST",url:r.parentObject().raw.labels,data:JSON.stringify({key:i.key,value:s?s:null})}).fail(function(e){n.alertError(e,"Error saving label","Errors saving label for "+i.key+":<br>")}))}),e.when.apply(this,t).done(function(){n.growlAlert("Successfully saved labels!","success"),r.newLabels([]),r.reload()})}})});