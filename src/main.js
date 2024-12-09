/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Import Vuetify and the dialog plugin. The line below was added manually. Alternatively, this can be added in plugins/index.js
import VuetifyUseDialog from 'vuetify-use-dialog';

const app = createApp(App);

// Use Vuetify and the dialog plugin. The line below was added manually Alternatively, this can be added in plugins/index.js
app.use(VuetifyUseDialog);

registerPlugins(app)

app.mount('#app')