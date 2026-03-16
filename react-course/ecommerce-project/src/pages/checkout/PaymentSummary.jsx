import {Money} from '../../assets/utils/money'

export function PaymentSummary({paymentSummary}){
    return(
        <div className="payment-summary">
                    <div className="payment-summary-title">
                    Payment Summary
                    </div>
                    {paymentSummary && (<>
                    <div className="payment-summary-row">
                    <div>Items ({paymentSummary.totalItems}):</div>
                    <div className="payment-summary-money">{`$${Money(paymentSummary.productCostCents)}`}</div>
                    </div>

                    <div className="payment-summary-row">
                    <div>Shipping &amp; handling:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.shippingCostCents)}</div>
                    </div>

                    <div className="payment-summary-row subtotal-row">
                    <div>Total before tax:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostBeforeTaxCents)}</div>
                    </div>

                    <div className="payment-summary-row">
                    <div>Estimated tax (10%):</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostBeforeTaxCents/10)}</div>
                    </div>

                    <div className="payment-summary-row total-row">
                    <div>Order total:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostCents)}</div>
                    </div>

                    <button className="place-order-button button-primary">
                    Place your order
                    </button></>)}
                </div>
    )
}