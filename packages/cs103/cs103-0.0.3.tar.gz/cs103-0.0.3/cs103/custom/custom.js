define([
    'base/js/events'
], function(events) {
    events.on('app_initialized.NotebookApp', function() {
        // Add 'Run all' button to toolbar
        IPython.toolbar.add_buttons_group([
            {
                'label' : 'run',
                'icon': 'fa-play',
                'callback' : function() { IPython.notebook.execute_all_cells() }
            }
        ]);

        // Add global keyboard shortcut to run all (Cmd/Ctrl+R)
        IPython.keyboard_manager.actions._actions['jupyter-notebook:run-all-cells'] = {
            handler: function(env) { env.notebook.execute_all_cells() }
        };
        IPython.keyboard_manager.command_shortcuts.add_shortcut(
            'cmdtrl-r', 'jupyter-notebook:run-all-cells'
        );
        IPython.keyboard_manager.edit_shortcuts.add_shortcut(
            'cmdtrl-r', 'jupyter-notebook:run-all-cells'
        );
    });
});
