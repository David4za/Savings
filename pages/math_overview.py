import streamlit as st

st.title("How the math works")
st.caption(
    "A plain-language guide to the formulas and assumptions behind each calculator. "
    "No finance degree required."
)

st.markdown("---")

# ---- Shared building block ----

st.markdown("### The rate conversion (used everywhere)")
st.markdown(
    """
Every calculator asks for an **expected annual return** (for example 7%). Investments compound
month by month, so we first convert that yearly figure into an equivalent **monthly rate**.

We treat the annual rate as an *effective* yearly return — meaning €1 left invested for one
full year would grow by exactly that percentage. The monthly rate is chosen so that twelve
months of compounding match the annual figure:
"""
)
st.latex(r"r_{\text{monthly}} = (1 + r_{\text{annual}})^{1/12} - 1")
st.info(
    "Example: 7% per year becomes about 0.565% per month — not simply 7 ÷ 12. "
    "Compounding makes the monthly slice slightly smaller than the naive division."
)

st.markdown("---")

# ---- Fixed income plan ----

st.markdown("### Fixed Income Plan — growing your savings")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Monthly savings (future value of an annuity)**")
    st.markdown(
        """
You enter a fixed amount saved **at the end of each month**. The calculator adds up how
those deposits grow with compound interest over your chosen horizon.
"""
    )
    st.latex(
        r"FV_{\text{monthly}} = P \times \frac{(1 + r_{\text{monthly}})^{n} - 1}{r_{\text{monthly}}}"
    )
    st.markdown(
        """
- **P** — monthly saving  
- **n** — total months (years × 12)  
- If the rate is 0%, this simplifies to **P × n** (no growth, just adding up deposits).
"""
    )

with col_right:
    st.markdown("**One-off lump sums**")
    st.markdown(
        """
Each lump sum is invested at the year you choose (“Add after year”). From that point it
compounds monthly until the end of the plan:
"""
    )
    st.latex(r"FV_{\text{lump}} = \text{amount} \times (1 + r_{\text{monthly}})^{\text{months remaining}}")
    st.markdown(
        """
Several lump sums are calculated separately and added together. The **Total Savings**
figure is monthly savings growth plus all lump-sum growth.
"""
    )

st.markdown("**Inflation-adjusted value**")
st.markdown(
    """
The final balance is shown in *today’s purchasing power* by reversing average inflation
over the saving period:
"""
)
st.latex(
    r"\text{Real value} = \frac{FV_{\text{total}}}{(1 + \text{inflation})^{years}}"
)
st.markdown(
    """
**Total contributions** counts every euro you put in: monthly deposits plus lump sums.
**Interest earned** is simply the gap between the final balance and what you contributed.
"""
)

st.markdown("---")

# ---- Reverse plan ----

st.markdown("### Reverse engineering — monthly saving needed for a target")
st.markdown(
    """
This page runs the monthly-savings formula **backwards**. Given a target amount, return,
and time horizon, it solves for the fixed monthly deposit required — assuming **only**
regular monthly savings (no lump sums):
"""
)
st.latex(
    r"P = FV \times \frac{r_{\text{monthly}}}{(1 + r_{\text{monthly}})^{n} - 1}"
)
st.markdown(
    "When the return is 0%, the answer is simply **FV ÷ n** (spread the target evenly "
    "across all months)."
)

st.markdown("---")

# ---- Withdraw plan ----

st.markdown("### Withdraw Plan — how long your money lasts")
st.markdown(
    """
Starting from your opening balance, the model steps through **one month at a time**:

1. Withdraw the monthly amount (or whatever is left if the balance is almost gone).  
2. Apply one month of investment return to the **remaining** balance.  
3. Repeat until the balance reaches zero.
"""
)
st.markdown("**Inflation-adjusted balance** (for the chart) shows what the remaining "
            "nominal balance would be worth in today’s money:")
st.latex(
    r"\text{Adjusted balance} = \frac{\text{Balance}}{(1 + \text{inflation})^{\text{years elapsed}}}"
)
st.markdown(
    """
The monthly withdrawal amount stays **fixed in euros** — it does not increase with
inflation. Inflation only affects the “real value” line on the chart, not how much is
withdrawn each month.
"""
)

st.markdown("---")

# ---- Assumptions ----

st.markdown("### Assumptions baked into the models")
st.markdown(
    """
| Topic | What we assume |
| --- | --- |
| Returns | Smooth, constant average return every month — no market ups and downs. |
| Contributions | Fixed monthly amount, deposited at **month-end**. |
| Lump sums | Deposited at a **year boundary**; growth starts from that checkpoint. |
| Inflation (savings) | Applied once at the end to express final wealth in today’s money. |
| Inflation (withdrawals) | Shown on the chart only; withdrawals stay fixed in nominal euros. |
| Reverse calculator | Target is reached by monthly savings alone — no one-off deposits. |
"""
)

with st.expander("Timing details worth knowing"):
    st.markdown(
        """
**Lump sums vs monthly savings timing**  
Monthly deposits use end-of-month timing throughout. A lump sum set to “Add after year 5”
appears in the year-5 total with zero months of growth in that same year, then compounds
in later years. That matches a deposit at the **end** of year 5, not necessarily the
same day-of-month as each monthly contribution.

**Withdrawal order**  
Each month we subtract the withdrawal *before* applying interest. That is a slightly
conservative choice — the balance earns return on what is left after paying yourself.

**Safety cap**  
The withdraw simulation stops after 1,200 months (100 years) even if a tiny balance
remains, to avoid infinite loops.
"""
    )
