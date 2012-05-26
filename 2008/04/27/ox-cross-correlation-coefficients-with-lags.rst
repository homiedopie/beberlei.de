
Ox: Cross-correlation coefficients with lags
============================================

Working on the homework for my `Monetary Economics
class <http://mueller.gernot.googlepages.com/monetaryeconomics>`_ I
realized that `Ox <http://www.doornik.com>`_ has different mechanisms to
calculate correlation coefficients like Mathlab has.

Our assignement was to replicate the Dynamic Correlations graph in
`Walshs' Monetary Theory and
Policy <http://www.amazon.de/gp/redirect.html?ie=UTF8&location=http://www.amazon.de/Monetary-Theory-Policy-Carl-Walsh/dp/0262232316?ie=UTF8&s=books-intl-de&qid=1209289935&sr=8-1&site-redirect=de&tag=economystuden-21&linkCode=ur2&camp=1638&creative=6742>`_
for European Data, which shows the cross-correlation of different
monetary aggregates (M0,M1,M2) with GDP over lagging periods of -8 to +8
quarters.

What was missing for me to do that assignment in Ox was a function to
calculate cross-correlation coefficients for two vectors for a specified
lag length:

    ::

        #include <oxfloat.h>

        /**
         * Computes the cross-correlation coefficient for two vector series allowing
         * to optionally specify the number of positive and negative lags the ccc
         * should be calculated for.
         *
         * @author Benjamin Eberlei (kontakt at beberlei dot de)
         * @param vVarY Tx1 vector of variable related to
         * @param vVarX Tx1 vector of variable which is tested in different lags
         * @param lags Integer indicating the number of negative and positive lags.
         * @returns (1+lags*2)*1 vector of correlations from -lags to lags
         **/
        ccf(const vVarY, const vVarX, const lags)
        {
            // Generate positive and negative lags of given length and fill with NaN, so
            // that rows with not available numbers can be dropped from calculating the CCF later on.
            decl mXLag = lag0(vVarX, range(lags, -lags), M_NAN);

            decl mCorr, sCov;
            
            // initialize result vector holding one crosscorrelation per lag
            decl vCorrLags = zeros(1+lags*2, 1);

            // sadly there are no matrix operations to ease this computation, loop over all lags
            for(decl i = 0; i < 1+lags*2; i++) {
                mCorr = deleter(vVarY ~ mXLag[][i]); // stick y and current lagged x together and delete NaN rows

                // calculate covariance of both time series
                sCov = 1/(rows(mCorr)-1) * sumc( (mCorr[][0]-meanc(mCorr[][0]))' * (mCorr[][1]-meanc(mCorr[][1])) );

                // calculate correlation coefficient
                vCorrLags[i][0] = sCov / ( sqrt(varc(mCorr[][0])) * sqrt(varc(mCorr[][1])) );
            }

            return vCorrLags;
        }

It may prove useful to someone.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>