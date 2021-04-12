import FancyForm from './fancy-form';
import $ from 'jquery';

const NAME = 'donate';
const DATA_KEY = 'ja.donate';
const EVENT_KEY = `.${DATA_KEY}`;
const DATA_API_KEY = '.data-api';

const EVENT_SUBMIT_DATA_API = `submit${EVENT_KEY}${DATA_API_KEY}`;

const SELECTOR_DATA_FORM = 'form[data-donate]';

class DonateForm {
	constructor(element, config) {
		this._element = element;
		this._config = config;

		this._fancy_form = new FancyForm(this._element);
	}

	submit() {
		const $form = $(this._element);
		const csrfToken = $form.find('[name=csrfmiddlewaretoken]').val();

		fetch($form.attr('action'), {
			body: new FormData(this._element),
			method: "POST",
			headers: {'X-CSRFToken': csrfToken},
		})
		.then((response) => {
			return response.json();
		})
		.then((session) => {
			return window.stripe.redirectToCheckout({ sessionId: session.id });
		})
		.then((result) => {
			// If redirectToCheckout fails due to a browser or network
			// error, you should display the localized error message to your
			// customer using error.message.
			this._fancy_form.addFormError(result.error.message);
		})
		.catch((error) => {
			this._fancy_form.addFormError(error);
		});
	}

	static jQueryInterface(method) {
		return this.each(function() {
			const $element = $(this);
			let instance = $element.data(DATA_KEY);

			const _config = {};

			if (!instance) {
				instance = new DonateForm(this, _config);
				$element.data(DATA_KEY, instance);
			}

			if (typeof method == 'string') {
				instance[method]();
			}
		});
	}
}

$(document).on(EVENT_SUBMIT_DATA_API, SELECTOR_DATA_FORM, function (event) {
	if (event.target.tagName === 'FORM') {
		event.preventDefault()
	}

    const $target = $(event.target)
    DonateForm.jQueryInterface.call($target, 'submit')
});

export default DonateForm;
