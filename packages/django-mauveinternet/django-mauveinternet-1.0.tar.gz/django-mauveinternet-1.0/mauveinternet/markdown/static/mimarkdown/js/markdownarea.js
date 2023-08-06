Event.observe(document, 'dom:loaded', function () {

	$$('textarea.markdown').each(function (t) {
		var outer = new Element('div', {'class': 'markdown_container'});
		t.insert({before: outer});
		outer.appendChild(t);	//move t
		var converter = new Showdown.converter;
		var preview = new Element('div', {'class': 'markdown_preview'}).update(converter.makeHtml(t.getValue()));
		preview.setStyle({width: (t.offsetWidth - 32) + 'px'});
		if (t.offsetHeight < 180)
			preview.setStyle({height: t.offsetHeight + 'px'});
		t.insert({before: preview});

		if (/show_preview=true/.match(document.cookie))
			preview.show();
		else
			preview.hide();

		var area = new Control.TextArea(t);
		var toolbar = new Control.TextArea.ToolBar(area);
		toolbar.container.className = 'markdown_toolbar';
		toolbar.container.setStyle({width: (t.offsetWidth - 6) + 'px'});
		t.setStyle({borderTop: 'none'});

		update_preview = function(value){
			var start = area.getSelectionStart();
			var src = area.getValue();

			// Markdown doesn't do anything special with @, which is why this approach works
			src = src.substr(0, start) + '@@EDITINGCARET@@' + src.substr(start);
			var html = converter.makeHtml(src).replace(/@@EDITINGCARET@@/, '<span class="caret"></span>');
			preview.update(html);
			var sel = preview.select('.caret')[0];
			if (sel)
			{
				preview.scrollTop = sel.cumulativeOffset().top - preview.cumulativeOffset().top - 30;
			}
		};

		//preview of markdown text
		new Form.Element.Observer(t, 0.3, update_preview);
		//area.observe('change', update_preview);
		Event.observe(area.element, 'click', update_preview);
		Event.observe(area.element, 'keypress', function (ev) {
			if (ev.keyCode == 13 && (ev.ctrlKey || ev.metaKey)) {
				area.replaceSelection('  \n');
				Event.stop(ev);
			}
		}.bindAsEventListener(area.element));
		toolbar.addButton('Bold',function(){
			this.wrapSelection('**','**');
		},{
			className: 'markdown_bold_button',
			title: 'Bold'
		});

		//buttons
		toolbar.addButton('Italics',function(){
			this.wrapSelection('*','*');
		},{
			className: 'markdown_italic_button',
			title: 'Italic'
		});

		toolbar.addButton('Link',function(){
			LinkDialog.init(area);
			return;
			var selection = this.getSelection();
			var response = prompt('Enter Link URL','');
			if(response == null)
				return;
			this.replaceSelection('[' + (selection == '' ? 'Link Text' : selection) + '](' + (response == '' ? 'http://link_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');
		},{
			className: 'markdown_link_button',
			title: 'Insert Link'
		});

//		toolbar.addButton('Image',function(){
//			var selection = this.getSelection();
//			var response = prompt('Enter Image URL','');
//			if(response == null)
//				return;
//			this.replaceSelection('![' + (selection == '' ? 'Image Alt Text' : selection) + '](' + (response == '' ? 'http://image_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');
//		},{
//			className: 'markdown_image_button',
//			title: 'Insert Image'
//		});

		toolbar.addButton('Heading',function(){
			var selection = this.getSelection();
			this.replaceSelection("\n" + selection + "\n" + $R(0, Math.min(10, selection.length)).collect(function(){return '-';}).join('') + "\n");
		},{
			className: 'markdown_heading_button',
			title: 'Heading'
		});

		toolbar.addButton('Unordered List',function(event){
			if (this.getSelection().match(/^\*\s/m)) {
				this.collectFromEachSelectedLine(function(line){
					return line.replace(/^\*\s+/, '');
				});
			} else {
				this.collectFromEachSelectedLine(function(line){
					return line.replace(/^(\*\s+)?/, '* ');
				});
			}
		},{
			className: 'markdown_unordered_list_button',
			title: 'Unordered List'
		});

		toolbar.addButton('Ordered List',function(event){
			if (this.getSelection().match(/^\d+\.\s/m)) {
				this.collectFromEachSelectedLine(function(line){
					return line.replace(/^\d+\.\s+/, '');
				});
			}
			else {
				var i = 0;

				this.collectFromEachSelectedLine(function(line){
					return line.replace(/^(\d+\.\s+)?/, ++i + '. ');
				});
			}
		},{
			className: 'markdown_ordered_list_button',
			title: 'Ordered List'
		});

		toolbar.addButton((preview.visible()) ? 'Hide Preview' : 'Show Preview', function () {
			preview.toggle();
			toolbar.container.select('.markdown_toggle_preview')[0].update(preview.visible() ? 'Hide Preview' : 'Show Preview');
			document.cookie = 'show_preview=' + ((preview.visible()) ? 'true' : 'false') + ';max-age=' + (60*60*24*365);
		} , {
			className: 'markdown_toggle_preview'
		});

		toolbar.addButton('Help', function () {
			window.open('http://daringfireball.net/projects/markdown/syntax');
		} , {
			className: 'markdown_help_button',
			title: 'Help'
		});

//		toolbar.addButton('Block Quote',function(event){
//			this.collectFromEachSelectedLine(function(line){
//				return event.shiftKey ? line.replace(/^\> /,'') : '> ' + line;
//			});
//		},{
//			className: 'markdown_quote_button'
//		});
	});
});

var LinkDialog = {
	init: function(textarea) {
		LinkDialog.textarea = textarea;
		var cont = new Element('div', {id: 'link-dialog'});

		cont.update('<p>Please select what you would like to link to:</p>' +
'<p><input type="radio" name="link-dialog-type" id="link-dialog-type-internal" value="internal" checked="checked"/> <label for="link-dialog-type-internal">A page within this site:</label>' +
'<select id="link-dialog-model"></select><select id="link-dialog-inst"></select></p>' +
'<p><input type="radio" name="link-dialog-type" id="link-dialog-type-external" value="external" /> <label for="link-dialog-type-external">Another site on the web:</label>' +
'<input type="text" id="link-dialog-abslink" value="http://" /></p>' +
'<p><input type="radio" name="link-dialog-type" id="link-dialog-type-email" value="email" /> <label for="link-dialog-type-email">E-mail address:</label>' +
'<input type="text" id="link-dialog-emaillink" value="" /></p>' +
'<div class="buttons"><button id="link-dialog-insert">Insert</button><button id="link-dialog-cancel">Cancel</button></div>'
);
		document.body.appendChild(cont);
		var at = $(textarea.element).cumulativeOffset();
		cont.setStyle({left: (at.left + 30) + 'px', top: (at.top + (textarea.element.offsetHeight - cont.offsetHeight)/2) + 'px'});
		new Ajax.Request('/admin/markdown/links', {method: 'GET'})
		LinkDialog.modelwatcher = new Form.Element.Observer('link-dialog-model', 0.2, LinkDialog.refreshInstances);
		Event.observe('link-dialog-abslink', 'focus', function () { $('link-dialog-abslink').select();});
		Event.observe('link-dialog-insert', 'click', LinkDialog.insertAndClose);
		Event.observe('link-dialog-cancel', 'click', LinkDialog.close);
	},

	insertAndClose: function () {
		if ($('link-dialog-type-internal').checked) {
			var link = 'internal:' + $F('link-dialog-model') + '/' + $F('link-dialog-inst');
			var selected = $('link-dialog-inst').childElements().find(function (x) {return x.selected;});
			LinkDialog.insert(link, selected.firstChild.nodeValue);
		} else if ($('link-dialog-type-email').checked) {
			LinkDialog.insert('mailto:' + $F('link-dialog-emaillink'));
		} else {
			LinkDialog.insert($F('link-dialog-abslink'));
		}

		LinkDialog.close();
	},

	insert: function (link, name) {
		var selection = LinkDialog.textarea.getSelection();
		LinkDialog.textarea.replaceSelection('[' + (selection == '' ? ((name) ? name : link) : selection) + '](' + link.replace(/^(?![a-z-]+:)/, 'http://') + ')');
	},

	close: function () {
		LinkDialog.modelwatcher.stop();
		$('link-dialog').remove();
	},

	updateModels: function(options) {
		for (i in options) {
			$('link-dialog-model').appendChild(new Element('option', {value: i}).update(options[i]));
		}
	},

	updateInstances: function(options) {
		$('link-dialog-inst').update('');
		for (i in options) {
			$('link-dialog-inst').appendChild(new Element('option', {value: i}).update(options[i]));
		}
	},

	refreshInstances: function(el, value) {
		new Ajax.Request('/admin/markdown/links?model=' + value, {method: 'GET'})
	}
};
