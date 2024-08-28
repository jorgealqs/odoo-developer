/** @odoo-module **/

import { Component, useState } from "@odoo/owl"

export class Playground extends Component {
    static template = "awesome_owl.playground_prueba"

    setup() {
        this.state = useState({ value: 1 })
    }

    increment() {
        this.state.value++
    }

}
