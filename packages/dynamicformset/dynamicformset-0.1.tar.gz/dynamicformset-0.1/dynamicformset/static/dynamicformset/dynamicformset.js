jQuery(function($) {
    $.widget("ui.dynamicformset", {
        // Default options
        options: {
            can_order: true,
            can_delete: true,
            min: 0,
            max: 1000,
            prefix: '',
            btn_class: 'dynamicformset-add',
            row_class: 'dynamicformset-row',
            sample_class: 'dynamicformset-sample',
            remove_class: 'dynamicformset-clear',
            draggable_class: 'dynamicformset-sort'
        },

        _create: function() {
            var self = this;

            this._deletable();
            this._sortable();

            this.element.on('click', '.'+this.options.btn_class, function() {
                self.add();
            });
        },

        /**
         * Make rows deletable
         * @private
         */
        _deletable: function()
        {
            if (!this.options.can_delete) {
                return;
            }

            var self = this,
                clear_selector = '.' + this.options.row_class + ' .' + this.options.remove_class;

            self.element.on('click', clear_selector, function (evt) {
                evt.preventDefault();
                var row = $(this).parent(self._rowSelector());
                self.remove(row);
                return false;
            });
        },

        /**
         * Make rows sortable
         * @private
         */
        _sortable: function()
        {
            if (!this.options.can_order) {
                return;
            }

            var self = this;

            this.element
                .sortable({
                    cursor: "ns-resize",
                    axis: "y",
                    handle: '.'+this.options.draggable_class,
                    containment: "parent",
                    items: '>.'+this.options.row_class,
                    placeholder: "sortable-item-highlight",
                    forcePlaceholderSize: true,
                    update: function (evt, ui) {
                        self._updateOrderIndex();
                        self._trigger("reordered", evt, ui);
                    }
                });
        },

        /**
         * Update order index after rows are re-ordered
         * @private
         */
        _updateOrderIndex: function()
        {
            this.element.find(this.options.row_class).find('.order_index').each(function(i, el) {
                $(el).val(i);
            });
        },

        /**
         * Check minimum and maximum number of rows allowed
         * @returns {number}
         * @private
         */
        _checkLimits: function()
        {
            var count = this.element.find(this._rowSelector()).size();
            if (count <= this.options.min) return -1;
            if (count >= this.options.max) return 1;
            return 0;
        },

        _rowSelector: function()
        {
            return '.' + this.options.row_class;
        },

        /**
         * Add new row
         */
        add: function()
        {
            // Maximum limit reached
            if (this._checkLimits() > 0)
                return false;

            var last_row = this.element.find(this._rowSelector()).last(),
                new_row = this.element.find('.' + this.options.sample_class).first().clone();

            new_row
                .addClass(this.options.row_class)
                .removeClass(this.options.sample_class);

            // Append after last row
            if (last_row.size()) {
                new_row.insertAfter(last_row);
            }
            // Insert before "add" button
            else
            {
                var btn = this.element.find('.' + this.options.btn_class);
                new_row.insertBefore(btn);
            }

            this._updateInputIndex(new_row);

            this._trigger("added", null, new_row);
            return new_row;
        },

        /**
         * Remove row
         */
        remove: function (row) {
            // Minimum limit reached
            if (this._checkLimits() < 0)
                return false;

            row.hide();

            // Mark form as deleted
            row.find('.delete_flag').val(1);

            this._trigger("deleted", null, row);
        },


        /**
         * Update indexes in newly created form and management form
         * @param form - newly created form
         */
        _updateInputIndex: function (form) {
            var prefix = this.options.prefix,
                total_forms = $('#id_'+prefix+'-TOTAL_FORMS'),
                forms_count = parseInt(total_forms.val()),
                regex = new RegExp('(' + prefix + '-__prefix__+)'),
                replacement = prefix + '-' + forms_count,
                // List of attributes to update
                attributes = ['for', 'id', 'name'];

            // Go through all child elements
            $(form).find('*').each(function (idx) {
                var el = $(this);
                $.each(attributes, function (i, name) {
                    var val = el.attr(name);
                    if (val) {
                        el.attr(name, val.replace(regex, replacement))
                    }
                })
            });

            // Update total number of forms
            total_forms.val(forms_count + 1);
        }

    });

    // Automatically initialize
    $('.dynamicformset').each(function(index) {
        var el = $(this);
        el.dynamicformset({
            order: parsePyBool(el.data('order')),
            delete: parsePyBool(el.data('delete')),
            min: parseInt(el.data('min')),
            max: parseInt(el.data('max')),
            prefix: el.data('prefix')
        });
    });

    function parsePyBool(v)
    {
        return (v == 'True')
    }
});
