=================
Booster Generator
=================
.. image:: https://travis-ci.org/Derfirm/booster_generator.svg?branch=master
    :target: https://travis-ci.org/Derfirm/booster_generator

To use (with caution), simply do::

    >>> cards = [(u'neut_u_modulehealer', u'1'), (u'terr_t_PrecisionStrike', u'2'), (u'terr_t_PulseBarrage', u'3'),(u'terr_t_NuclearStrike', u'4'),\
            (u'shan_u_NaninteSwarm', u'3'), (u'shan_t_CorruptTransform', u'3'), (u'shan_u_ParasiticThrall', u'5'), (u'shan_t_Infestation', u'2')]
    >>> boosterpack = BoosterGenerator(cards)
    >>> print (boosterpack.generate())
