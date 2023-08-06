Faceted.taxonomySeparator = ' » ';
Faceted.taxonomyAllString = ' (tous)';

Faceted.initSelect2 = function(select) {
  if (select.hasClass('init-select2-done')) {
    return;
  }
  var options = {'children': {}};
  jQuery.map(select.find('option'), function(option, index) {
    var parts = option.title.split(Faceted.taxonomySeparator);
    var current = options;
    for(var j=0; j<parts.length; j++) {
      if(!current.children[parts[j]]) {
        current.children[parts[j]] = {children: {}};
      }
      current = current.children[parts[j]];
    }
    current.value = option.value;
    current.title = parts[parts.length-1];
    if(option.selected) {
      current.selected = true;
    }
  });
  select.find('option').remove();
  var html = '';
  function create_options(sub_option, depth) {
    var selected = '';
    if(sub_option.selected) {
      selected = ' selected="selected"';
    }
    if (Object.keys(sub_option.children).length > 0) {
      html += '<optgroup class="depth-' + depth + '" label="' + sub_option.title + '">';
      html += '<option title="' + sub_option.title + '" value="' + sub_option.value + '"' + selected + '>' + sub_option.title + Faceted.taxonomyAllString + '</option>';
      for(var child in sub_option.children) {
        create_options(sub_option.children[child], depth + 1);
      }
      html += '</optgroup>';
    } else {
      if(sub_option.value) {
        html += '<option title="' + sub_option.title + '" value="' + sub_option.value + '"' + selected + '>' + sub_option.title + '</option>';
      }
    }
  }
  for (var child in options.children) {
    create_options(options.children[child], 0);
  }
  select.append(html);
  // select2 doesn't seem to like '-' in the id...
  // you get the error "TypeError: b[0] is undefined"
  select.select2();
  select.siblings('button[data-select2-open]').click(function(){
    jQuery('#' + jQuery(this).data('select2-open')).select2('open');
  });
  select.siblings('.select2-container')[0].style.minWidth = '200px';
  select.addClass('init-select2-done')
};


jQuery(document).ready(function() {
  // very important to have 'select' in the selector to avoid
  // error "uncaught exception: query function not defined for Select2 someid"
  // when it actually process a div.z3cform-select2
  jQuery('select.z3cform-select2').each(function(i, elem) {
    Faceted.initSelect2($(elem));
  });
  // jQuery('button[data-select2-open]').hide();
});


/* Select Widget
*/
Faceted.Select2Widget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + this.wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);
  this.selected = [];

  // Faceted version
  this.version = '';
  var version = jQuery('#faceted-version');
  if(version){
    this.version = version.text();
  }

  // Handle change
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  var js_widget = this;
  this.select.change(function(evt){
    js_widget.select_change(this, evt);
  });

  // Default value
  var value = this.select.val();
  if(value){
    this.selected = jQuery("option[value='" + value + "']", js_widget.widget);
    Faceted.Query[this.wid] = [value];
  }

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
  if(this.widget.hasClass('faceted-count')){
    var sortcountable = this.widget.hasClass('faceted-sortcountable');
    jQuery(Faceted.Events).bind(Faceted.Events.QUERY_INITIALIZED, function(evt){
      js_widget.count(sortcountable);
    });
    jQuery(Faceted.Events).bind(Faceted.Events.FORM_DO_QUERY, function(evt, data){
      if(data.wid == js_widget.wid || data.wid == 'b_start'){
        return;
      }
      js_widget.count(sortcountable);
    });
  }
  Faceted.initSelect2(this.select);
};

Faceted.Select2Widget.prototype = {
  select_change: function(element, evt){
    if(!jQuery(element).val()){
      element = null;
    }
    this.do_query(element);
  },

  do_query: function(element){
    if(!element){
      this.selected = [];
      return Faceted.Form.do_query(this.wid, []);
    }else{
      var value = jQuery.map(
        jQuery('#' + this.wid).select2('data'),
        function(option) {return option.id;}
      );
      return Faceted.Form.do_query(this.wid, value);
    }
  },

  reset: function(){
    this.select.val("");
    this.selected = [];
  },

  synchronize: function(){
    var current_values = Faceted.Query[this.wid];
    if(!current_values){
      this.reset();
      return;
    }
    if(current_values){
      var context = this;
      var selected = [];
      jQuery.each(current_values, function(i, value){
        var option_el = jQuery("option[value='" + value + "']", context.widget);
        jQuery(option_el).attr('selected', 'selected');
        selected.push(option_el);
      });
      if(!selected.length){
        context.reset();
      }else{
        context.selected = selected;
      }
    }
  },

  criteria: function(){
    var html = [];
    var title = this.criteria_title();
    var body = this.criteria_body();
    if(title){
      html.push(title);
    }
    if(body){
      html.push(body);
    }
    return html;
  },

  criteria_title: function(){
    if(!this.selected.length){
      return '';
    }

    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + this.wid);
    link.attr('title', 'Remove ' + this.title + ' filters');
    var widget = this;
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });

    var html = jQuery('<dt>');
    html.attr('id', 'criteria_' + this.wid + '_label');
    html.append(link);
    html.append('<span>' + this.title + '</span>');
    return html;
  },

  criteria_body: function(){
    if(!this.selected.length){
      return '';
    }

    var widget = this;
    var html = jQuery('<dd>');
    var span = jQuery('<span class="facted-select-criterion">');
    html.attr('id', 'criteria_' + this.wid + '_entries');
    var element = jQuery(this.selected);
    var value = element.val();
    var label = element.attr('title');
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_' + value);
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);

    return html;
  },

  criteria_remove: function(){
    this.select.val('');
    this.do_query();
  },

  count: function(sortcountable){
    var query = Faceted.SortedQuery();
    query.cid = this.wid;
    if(this.version){
      query.version = this.version;
    }

    var context = this;
    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_START, {wid: context.wid});
    jQuery.getJSON(Faceted.BASEURL + '@@faceted_counter', query, function(data){
      context.count_update(data, sortcountable);
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_STOP, {wid: context.wid});
    });
  },

  count_update: function(data, sortcountable){
    var context = this;
    var select = jQuery('select', context.widget);
    var options = jQuery('option', context.widget);
    var current_val = select.val();
    jQuery(options).each(function(){
      var option = jQuery(this);
      option.removeClass('faceted-select-item-disabled');
      option.attr('disabled', false);
      var key = option.val();

      var value = data[key];
      value = value ? value : 0;
      var option_txt = option.attr('title');
      option_txt += ' (' + value + ')';

      option.html(option_txt);
      if(sortcountable){
        option.data('count', value);
      }
      if(!value){
        option.attr('disabled', 'disabled');
        option.addClass('faceted-select-item-disabled');
      }
    });
    if(sortcountable){
      options.detach().sort(function(x, y) {
        var a = jQuery(x).data('count');
        var b = jQuery(y).data('count');
        return b - a;
      });
      select.append(options);
      select.val(current_val);
    }
  }
};

Faceted.initializeSelect2Widget = function(evt){
  jQuery('div.faceted-select-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.Select2Widget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeSelect2Widget);
});
