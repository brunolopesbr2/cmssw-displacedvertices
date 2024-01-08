#!/usr/bin/env python

from JMTucker.Tools.Sample import *
from JMTucker.Tools.CMSSWTools import json_path

########################################################################

def _model(sample):
    s = sample if type(sample) == str else sample.name
    if s.startswith('Stealth'):
        return s.split('_')[0]
    else:
        return s.split('_tau')[0]

def _tau(sample):
    s = sample if type(sample) == str else sample.name
    is_um = '0um_' in s

    # parse string to extract the lifetime
    if s.startswith('Stealth'):
        x = s[s.index('tau')+4:s.index('201')-1]
    else:
        x = s[s.index('tau')+3:s.index('um_' if is_um else 'mm_')]
    # special case where the string isn't directly castable to a number!
    if x == '0p1' : x = 0.1
    if x == '0p01': x = 0.01

    x = float(x)
    if not is_um:
        x *= 1000
    return x

def _mass(sample):
    s = sample if type(sample) == str else sample.name

    if s.startswith('Stealth'):
        x = s.find('mStop')
        y = s.find('_',x+7)
        if y == -1:
            y = len(s)
        return int(s[x+6:y])
    else:
        x = s.index('_M')
        y = s.find('_',x+1)
        if y == -1:
            y = len(s)
        return int(s[x+2:y])

def _decay(sample):
    s = sample if type(sample) == str else sample.name
    if s.startswith('of_'):
        s = s[3:]
    decay = {
        'mfv_neu': r'\tilde{N} \rightarrow tbs',
        'xx4j': r'X \rightarrow q\bar{q}',
        'mfv_ddbar': r'\tilde{g} \rightarrow d\bar{d}',
        'mfv_neuuds': r'\tilde{N} \rightarrow uds',
        'mfv_neuudmu': r'\tilde{N} \rightarrow u\bar{d}\mu^{\minus}',
        'mfv_neuude': r'\tilde{N} \rightarrow u\bar{d}e^{\minus}',
        'mfv_neucdb': r'\tilde{N} \rightarrow cdb',
        'mfv_neucds': r'\tilde{N} \rightarrow cds',
        'mfv_neutbb': r'\tilde{N} \rightarrow tbb',
        'mfv_neutds': r'\tilde{N} \rightarrow tds',
        'mfv_neuubb': r'\tilde{N} \rightarrow ubb',
        'mfv_neuudb': r'\tilde{N} \rightarrow udb',
        'mfv_neuudtu': r'\tilde{N} \rightarrow u\bar{d}\tau^{\minus}',
        'mfv_xxddbar': r'X \rightarrow d\bar{d}',
        'mfv_stopdbardbar': r'\tilde{t} \rightarrow \bar{d}\bar{d}',
        'mfv_stopbbarbbar': r'\tilde{t} \rightarrow \bar{b}\bar{b}',
        'mfv_splitSUSY' : r'\tilde{g} \rightarrow qq\tilde{\chi}',
        'mfv_HtoLLPto4j': r'H \rightarrow LLP \rightarrow jjjj',
        'mfv_HtoLLPto4b': r'H \rightarrow LLP \rightarrow bbbb',
        'mfv_ZprimetoLLPto4j': r'Zprime \rightarrow LLP \rightarrow jjjj',
        'mfv_ZprimetoLLPto4b': r'Zprime \rightarrow LLP \rightarrow bbbb',
        'StealthSHH': r'stop \rightarrow St \rightarrow bbt',
        'StealthSYY': r'stop \rightarrow St \rightarrow ggt',
        }[_model(s)]
    year = int(s.rsplit('_')[-1])
    assert 2015 <= year <= 2018
    decay += ' (%i)' % year
    return decay

def _latex(sample):
    tau = _tau(sample) 
    if tau < 1000: 
        tau = '%3i\mum' % tau
    else:
        assert tau % 1000 == 0
        tau = '%4i\mm' % (tau/1000)
    return r'$%s$,   $c\tau = %s$, $M = %4s\GeV$' % (_decay(sample), tau, _mass(sample))

def _rp(sample):
    s = sample if type(sample) == str else sample.name

    rp = False
    rp_list = ['ZH', 'WmH', 'WpH', 'Stealth']
    for i in rp_list :
        if s.startswith(i) :     
            rp = True
    return rp

def _set_signal_stuff(sample):
    sample.is_signal = True
    sample.model = _model(sample)
    sample.decay = _decay(sample)
    sample.tau = _tau(sample)
    sample.mass = _mass(sample)
    sample.latex = _latex(sample)
    sample.xsec = 1e-3
    sample.is_private = sample.dataset.startswith('/mfv_')
    sample.is_rp = _rp(sample)
    if sample.is_private:
        sample.dbs_inst = 'phys03'
        sample.condor = True
        sample.xrootd_url = xrootd_sites['T3_US_FNALLPC']

########################################################################

########
# 2017 MC
########

qcd_samples_2017 = [
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                 48042655, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.351e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v1/AODSIM', 16882838, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3),
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',         11634434, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0),
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',           5941306, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=20.2),
    ]

ttbar_samples_2017 = [
    MCSample('ttbarht0600_2017', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',   81565576, nice='t#bar{t}, 600 < H_{T} < 800 GeV',   color=600, syst_frac=0.15, xsec=1.817),
    MCSample('ttbarht0800_2017', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',  40248127, nice='t#bar{t}, 800 < H_{T} < 1200 GeV',  color=601, syst_frac=0.15, xsec=0.7520),
    MCSample('ttbarht1200_2017', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 13214871, nice='t#bar{t}, 1200 < H_{T} < 2500 GeV', color=602, syst_frac=0.15, xsec=0.1313),
    MCSample('ttbarht2500_2017', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v3/AODSIM',   5155687, nice='t#bar{t}, H_{T} > 2500 GeV',        color=603, syst_frac=0.15, xsec=1.41e-3),
    ]

bjet_samples_2017 = [
    MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 59569132, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5),
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM', 56854504, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=2.998e4),
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',    155582358, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=832.),
    MCSample('ttHbb_2017',     '/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',      10055168, nice='ttHbb', color=1, syst_frac=0.20, xsec=0.5269), # FIXME note syst_frac here isn't correct here or below, but is probably irrelevant
    MCSample('ttZ_2017',       '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',                        9771320, nice='ttZ', color=1, syst_frac=0.20, xsec=0.5407),
    MCSample('ttZext_2017',    '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v3/AODSIM',                   8536618, nice='ttZ', color=1, syst_frac=0.20, xsec=0.5407),
    MCSample('singletop_tchan_top_2017',    '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',             5982064, nice='singletop t-channel top', color=1, syst_frac=0.20, xsec=113.3),
    MCSample('singletop_tchan_antitop_2017','/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v2/AODSIM', 3675910, nice='singletop t-channel antitop', color=1, syst_frac=0.20, xsec=67.91),
    ]

bjet_samples_sum_2017 = [
    SumSample('ttZsum_2017', bjet_samples_2017[4:6]),
]

leptonic_samples_2017 = [
    #MCSample('ttbar_2017',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 155582358, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.), # inclusive ttbar sample has been moved to bjet_samples_2017
    MCSample('wjetstolnu_2017',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',                    33073306, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.28e4),
    MCSample('wjetstolnuext_2017',    '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v2/AODSIM',               44652002, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.28e4),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v2/AODSIM',                  39521230, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
   #MCSample('dyjetstollM10ext_2017', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v1/AODSIM',      39536839, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-RECOSIMstep_94X_mc2017_realistic_v10-v1/AODSIM',          48675378, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    MCSample('dyjetstollM50ext_2017', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/AODSIM',     49313842, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    MCSample('qcdmupt15_2017',        '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017RECOSIMstep_94X_mc2017_realistic_v11-v1/AODSIM',  21833984, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=5.23e8*4.57e-4),
   #MCSample('qcdempt015_2017',       '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         11215220, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.28e3*0.0018),
   #MCSample('qcdempt020_2017',       '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         11590942, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=5.58e8*0.0096),
   #MCSample('qcdempt030_2017',       '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         14766010, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.36e8*0.0730),
   #MCSample('qcdempt050_2017',       '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         10689785, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.98e7*0.1460),
   #MCSample('qcdempt080_2017',       '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',                  9104852, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=2.80e6*0.1250),
   #MCSample('qcdempt120_2017',       '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',                 8515107, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.77e5*0.1320),
   #MCSample('qcdempt170_2017',                                                                                                                                                 , nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.14e5*0.1650),
   #MCSample('qcdempt300_2017',       '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                        2898084, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=9.00e3*0.1500),
   #MCSample('qcdbctoept015_2017',                                                                                                                                              , nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.27e9*0.00020),
   #MCSample('qcdbctoept020_2017',    '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v1/AODSIM',                5831551, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=5.58e8*0.00059),
   #MCSample('qcdbctoept030_2017',    '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                              16073047, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.59e8*0.00255),
   #MCSample('qcdbctoept080_2017',    '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                             15999466, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.22e6*0.01183),
   #MCSample('qcdbctoept170_2017',    '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                             9847660, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.06e5*0.02492),
   #MCSample('qcdbctoept250_2017',    '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                            10115200, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=2.11e4*0.03375),
    ]

leptonic_samples_sum_2017 = [
    SumSample('wjetstolnusum_2017',    leptonic_samples_2017[ :2]),
   #SumSample('dyjetstollM10sum_2017', leptonic_samples_2017[2:4]),
    SumSample('dyjetstollM50sum_2017', leptonic_samples_2017[3:5]),
    ]

mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau000100um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('mfv_neu_tau000100um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99997),
    MCSample('mfv_neu_tau000300um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau000300um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau001000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau001000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau010000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau030000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99999),
    ]

mfv_stopdbardbar_samples_2017 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 95000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    ]

StealthSHH_samples_2017 = [ 
    MCSample('StealthSHH_mStop_300_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_0p01_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_0p1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_1_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_10_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_100_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_1000_2017', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8961124)
    ]

StealthSYY_samples_2017 = [ 
    MCSample('StealthSYY_mStop_300_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_0p01_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_0p1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_1_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_10_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_100_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_1000_2017', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 8343346)
    ]


#all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + StealthSHH_samples_2017 + StealthSYY_samples_2017

all_signal_samples_2017 = StealthSHH_samples_2017 + StealthSYY_samples_2017

for s in all_signal_samples_2017:
    _set_signal_stuff(s)

########
# 2018 MC
########

qcd_samples_2018 = [
    MCSample('qcdht0700_2018', '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  43523821, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.351e3),
    MCSample('qcdht1000_2018', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 15174716, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3),
    MCSample('qcdht1500_2018', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 11082955, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0),
    MCSample('qcdht2000_2018', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   5557453, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=20.2),
    ]

ttbar_samples_2018 = [
    MCSample('ttbarht0600_2018', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   14363689, nice='t#bar{t}, 600 < H_{T} < 800 GeV',   color=600, syst_frac=0.15, xsec=1.817),
    MCSample('ttbarht0800_2018', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  10462756, nice='t#bar{t}, 800 < H_{T} < 1200 GeV',  color=601, syst_frac=0.15, xsec=0.7520),
    MCSample('ttbarht1200_2018', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  2897601, nice='t#bar{t}, 1200 < H_{T} < 2500 GeV', color=602, syst_frac=0.15, xsec=0.1313),
    MCSample('ttbarht2500_2018', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   1451104, nice='t#bar{t}, H_{T} > 2500 GeV',        color=603, syst_frac=0.15, xsec=1.41e-3),
    ]

bjet_samples_2018 = [
    MCSample('qcdht0300_2018', '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 55094256, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5),
    MCSample('qcdht0500_2018', '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 55195716, nice='QCD, 500 < H_{T} < 700 GeV',  color=804, syst_frac=0.20, xsec=2.998e4),
    MCSample('ttbar_2018',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',  145295353, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]


mfv_signal_samples_2018 = [
    MCSample('mfv_neu_tau000100um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 96000),
    MCSample('mfv_neu_tau000100um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99998),
    MCSample('mfv_neu_tau010000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau010000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99999),
    MCSample('mfv_neu_tau030000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    ]

mfv_stopdbardbar_samples_2018 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 96000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    ]

StealthSHH_samples_2018 = [ 
    MCSample('StealthSHH_mStop_300_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_300_mS_75_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_500_mS_275_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_700_mS_475_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_900_mS_675_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1100_mS_875_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1300_mS_1075_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_100_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_0p01_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_0p1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_1_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_10_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_100_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876),
    MCSample('StealthSHH_mStop_1500_mS_1275_ctau_1000_2018', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8779876)
    ]
StealthSYY_samples_2018 = [ 
    MCSample('StealthSYY_mStop_300_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_300_mS_75_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_500_mS_275_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_700_mS_475_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_900_mS_675_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1100_mS_875_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1300_mS_1075_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_100_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_0p01_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_0p1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_1_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_10_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_100_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264),
    MCSample('StealthSYY_mStop_1500_mS_1275_ctau_1000_2018', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 8994264)
    ]

#all_signal_samples_2018 = mfv_signal_samples_2018 + mfv_stopdbardbar_samples_2018
all_signal_samples_2018 = StealthSHH_samples_2018 + StealthSYY_samples_2018

for s in all_signal_samples_2018:
    _set_signal_stuff(s)

# splitSUSY samples for LLP summary plot
mfv_splitSUSY_samples_2016 = [
    MCSample('mfv_splitSUSY_tau000000100um_M2400_100_2016', '/mfv_splitSUSY_tau000000100um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2016', '/mfv_splitSUSY_tau000001000um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2016', '/mfv_splitSUSY_tau000010000um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000100000um_M2400_100_2016', '/mfv_splitSUSY_tau000100000um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau001000000um_M2400_100_2016', '/mfv_splitSUSY_tau001000000um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau010000000um_M2400_100_2016', '/mfv_splitSUSY_tau010000000um_M2400_100_2016/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau100000000um_M2400_100_2016', '/mfv_splitSUSY_tau100000000um_M2400_100_2016/None/USER', 10000),
]

mfv_splitSUSY_samples_2017 = [
    MCSample('mfv_splitSUSY_tau000000100um_M2400_100_2017', '/mfv_splitSUSY_tau000000100um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2017', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2017', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000100000um_M2400_100_2017', '/mfv_splitSUSY_tau000100000um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau001000000um_M2400_100_2017', '/mfv_splitSUSY_tau001000000um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau010000000um_M2400_100_2017', '/mfv_splitSUSY_tau010000000um_M2400_100_2017/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau100000000um_M2400_100_2017', '/mfv_splitSUSY_tau100000000um_M2400_100_2017/None/USER', 10000),
]

mfv_splitSUSY_samples_2018 = [
    MCSample('mfv_splitSUSY_tau000000100um_M2400_100_2018', '/mfv_splitSUSY_tau000000100um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2018', '/mfv_splitSUSY_tau000001000um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2018', '/mfv_splitSUSY_tau000010000um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau000100000um_M2400_100_2018', '/mfv_splitSUSY_tau000100000um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau001000000um_M2400_100_2018', '/mfv_splitSUSY_tau001000000um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau010000000um_M2400_100_2018', '/mfv_splitSUSY_tau010000000um_M2400_100_2018/None/USER', 10000),
    MCSample('mfv_splitSUSY_tau100000000um_M2400_100_2018', '/mfv_splitSUSY_tau100000000um_M2400_100_2018/None/USER', 10000),

]

mfv_HtoLLPto4j_samples_2016 = [
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_150_2016', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_40_2016', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_250_2016', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_60_2016', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_350_2016', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_80_2016', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_150_2016', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_40_2016', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_250_2016', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_60_2016', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_350_2016', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_80_2016', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_150_2016', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_40_2016', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_250_2016', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_60_2016', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_350_2016', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_80_2016', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_150_2016', '/mfv_HtoLLPto4j_tau100mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_40_2016', '/mfv_HtoLLPto4j_tau100mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_250_2016', '/mfv_HtoLLPto4j_tau100mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_60_2016', '/mfv_HtoLLPto4j_tau100mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_350_2016', '/mfv_HtoLLPto4j_tau100mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_80_2016', '/mfv_HtoLLPto4j_tau100mm_M800_80_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_150_2016', '/mfv_HtoLLPto4j_tau10mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_40_2016', '/mfv_HtoLLPto4j_tau10mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_250_2016', '/mfv_HtoLLPto4j_tau10mm_M600_250_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_60_2016', '/mfv_HtoLLPto4j_tau10mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_350_2016', '/mfv_HtoLLPto4j_tau10mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_80_2016', '/mfv_HtoLLPto4j_tau10mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_100_2016', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_450_2016', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_150_2016', '/mfv_HtoLLPto4j_tau1mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_40_2016', '/mfv_HtoLLPto4j_tau1mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_250_2016', '/mfv_HtoLLPto4j_tau1mm_M600_250_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_60_2016', '/mfv_HtoLLPto4j_tau1mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_350_2016', '/mfv_HtoLLPto4j_tau1mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_80_2016', '/mfv_HtoLLPto4j_tau1mm_M800_80_2016/None/USER', 25000),
]

mfv_HtoLLPto4j_samples_2017 = [
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_150_2017', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_40_2017', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_250_2017', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_60_2017', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_350_2017', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_80_2017', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_150_2017', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_40_2017', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_250_2017', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_60_2017', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_350_2017', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_80_2017', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_150_2017', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_40_2017', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_250_2017', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_60_2017', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_350_2017', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_80_2017', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_150_2017', '/mfv_HtoLLPto4j_tau100mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_40_2017', '/mfv_HtoLLPto4j_tau100mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_250_2017', '/mfv_HtoLLPto4j_tau100mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_60_2017', '/mfv_HtoLLPto4j_tau100mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_350_2017', '/mfv_HtoLLPto4j_tau100mm_M800_350_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_80_2017', '/mfv_HtoLLPto4j_tau100mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_150_2017', '/mfv_HtoLLPto4j_tau10mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_40_2017', '/mfv_HtoLLPto4j_tau10mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_250_2017', '/mfv_HtoLLPto4j_tau10mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_60_2017', '/mfv_HtoLLPto4j_tau10mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_350_2017', '/mfv_HtoLLPto4j_tau10mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_80_2017', '/mfv_HtoLLPto4j_tau10mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_100_2017', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_450_2017', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_150_2017', '/mfv_HtoLLPto4j_tau1mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_40_2017', '/mfv_HtoLLPto4j_tau1mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_250_2017', '/mfv_HtoLLPto4j_tau1mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_60_2017', '/mfv_HtoLLPto4j_tau1mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_350_2017', '/mfv_HtoLLPto4j_tau1mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_80_2017', '/mfv_HtoLLPto4j_tau1mm_M800_80_2017/None/USER', 25000),
]

mfv_HtoLLPto4j_samples_2018 = [
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_150_2018', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M400_40_2018', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_250_2018', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M600_60_2018', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_350_2018', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau0p1mm_M800_80_2018', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_150_2018', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M400_40_2018', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_250_2018', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M600_60_2018', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_350_2018', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10000mm_M800_80_2018', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_150_2018', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M400_40_2018', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_250_2018', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M600_60_2018', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_350_2018', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1000mm_M800_80_2018', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_150_2018', '/mfv_HtoLLPto4j_tau100mm_M400_150_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau100mm_M400_40_2018', '/mfv_HtoLLPto4j_tau100mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_250_2018', '/mfv_HtoLLPto4j_tau100mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau100mm_M600_60_2018', '/mfv_HtoLLPto4j_tau100mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_350_2018', '/mfv_HtoLLPto4j_tau100mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau100mm_M800_80_2018', '/mfv_HtoLLPto4j_tau100mm_M800_80_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_150_2018', '/mfv_HtoLLPto4j_tau10mm_M400_150_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M400_40_2018', '/mfv_HtoLLPto4j_tau10mm_M400_40_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_250_2018', '/mfv_HtoLLPto4j_tau10mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau10mm_M600_60_2018', '/mfv_HtoLLPto4j_tau10mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_350_2018', '/mfv_HtoLLPto4j_tau10mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau10mm_M800_80_2018', '/mfv_HtoLLPto4j_tau10mm_M800_80_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_100_2018', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M1000_450_2018', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_150_2018', '/mfv_HtoLLPto4j_tau1mm_M400_150_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1mm_M400_40_2018', '/mfv_HtoLLPto4j_tau1mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_250_2018', '/mfv_HtoLLPto4j_tau1mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4j_tau1mm_M600_60_2018', '/mfv_HtoLLPto4j_tau1mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_350_2018', '/mfv_HtoLLPto4j_tau1mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4j_tau1mm_M800_80_2018', '/mfv_HtoLLPto4j_tau1mm_M800_80_2018/None/USER', 25000),
]

mfv_HtoLLPto4b_samples_2016 = [
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_150_2016', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_40_2016', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_250_2016', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_60_2016', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_350_2016', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_80_2016', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_150_2016', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_40_2016', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_250_2016', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_60_2016', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_350_2016', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_80_2016', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_150_2016', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_40_2016', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_250_2016', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_60_2016', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_350_2016', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_80_2016', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_150_2016', '/mfv_HtoLLPto4b_tau100mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_40_2016', '/mfv_HtoLLPto4b_tau100mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_250_2016', '/mfv_HtoLLPto4b_tau100mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_60_2016', '/mfv_HtoLLPto4b_tau100mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_350_2016', '/mfv_HtoLLPto4b_tau100mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_80_2016', '/mfv_HtoLLPto4b_tau100mm_M800_80_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_150_2016', '/mfv_HtoLLPto4b_tau10mm_M400_150_2016/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_40_2016', '/mfv_HtoLLPto4b_tau10mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_250_2016', '/mfv_HtoLLPto4b_tau10mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_60_2016', '/mfv_HtoLLPto4b_tau10mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_350_2016', '/mfv_HtoLLPto4b_tau10mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_80_2016', '/mfv_HtoLLPto4b_tau10mm_M800_80_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_100_2016', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_450_2016', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_150_2016', '/mfv_HtoLLPto4b_tau1mm_M400_150_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_40_2016', '/mfv_HtoLLPto4b_tau1mm_M400_40_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_250_2016', '/mfv_HtoLLPto4b_tau1mm_M600_250_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_60_2016', '/mfv_HtoLLPto4b_tau1mm_M600_60_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_350_2016', '/mfv_HtoLLPto4b_tau1mm_M800_350_2016/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_80_2016', '/mfv_HtoLLPto4b_tau1mm_M800_80_2016/None/USER', 25000),
]

mfv_HtoLLPto4b_samples_2017 = [
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_150_2017', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_40_2017', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_250_2017', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_60_2017', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_350_2017', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_80_2017', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_150_2017', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_40_2017', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_250_2017', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_60_2017', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_350_2017', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_80_2017', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_150_2017', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_40_2017', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_250_2017', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_60_2017', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_350_2017', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_80_2017', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_150_2017', '/mfv_HtoLLPto4b_tau100mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_40_2017', '/mfv_HtoLLPto4b_tau100mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_250_2017', '/mfv_HtoLLPto4b_tau100mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_60_2017', '/mfv_HtoLLPto4b_tau100mm_M600_60_2017/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_350_2017', '/mfv_HtoLLPto4b_tau100mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_80_2017', '/mfv_HtoLLPto4b_tau100mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_150_2017', '/mfv_HtoLLPto4b_tau10mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_40_2017', '/mfv_HtoLLPto4b_tau10mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_250_2017', '/mfv_HtoLLPto4b_tau10mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_60_2017', '/mfv_HtoLLPto4b_tau10mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_350_2017', '/mfv_HtoLLPto4b_tau10mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_80_2017', '/mfv_HtoLLPto4b_tau10mm_M800_80_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_100_2017', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_450_2017', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_150_2017', '/mfv_HtoLLPto4b_tau1mm_M400_150_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_40_2017', '/mfv_HtoLLPto4b_tau1mm_M400_40_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_250_2017', '/mfv_HtoLLPto4b_tau1mm_M600_250_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_60_2017', '/mfv_HtoLLPto4b_tau1mm_M600_60_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_350_2017', '/mfv_HtoLLPto4b_tau1mm_M800_350_2017/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_80_2017', '/mfv_HtoLLPto4b_tau1mm_M800_80_2017/None/USER', 25000),
]

mfv_HtoLLPto4b_samples_2018 = [
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_150_2018', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M400_40_2018', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_250_2018', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M600_60_2018', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_350_2018', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau0p1mm_M800_80_2018', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_150_2018', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M400_40_2018', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_250_2018', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M600_60_2018', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_350_2018', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10000mm_M800_80_2018', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_150_2018', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M400_40_2018', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_250_2018', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1000mm_M600_60_2018', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_350_2018', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1000mm_M800_80_2018', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau100mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_150_2018', '/mfv_HtoLLPto4b_tau100mm_M400_150_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau100mm_M400_40_2018', '/mfv_HtoLLPto4b_tau100mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_250_2018', '/mfv_HtoLLPto4b_tau100mm_M600_250_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M600_60_2018', '/mfv_HtoLLPto4b_tau100mm_M600_60_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_350_2018', '/mfv_HtoLLPto4b_tau100mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau100mm_M800_80_2018', '/mfv_HtoLLPto4b_tau100mm_M800_80_2018/None/USER', 23500),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_150_2018', '/mfv_HtoLLPto4b_tau10mm_M400_150_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M400_40_2018', '/mfv_HtoLLPto4b_tau10mm_M400_40_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_250_2018', '/mfv_HtoLLPto4b_tau10mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M600_60_2018', '/mfv_HtoLLPto4b_tau10mm_M600_60_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_350_2018', '/mfv_HtoLLPto4b_tau10mm_M800_350_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau10mm_M800_80_2018', '/mfv_HtoLLPto4b_tau10mm_M800_80_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_100_2018', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M1000_450_2018', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_150_2018', '/mfv_HtoLLPto4b_tau1mm_M400_150_2018/None/USER', 24000),
MCSample('mfv_HtoLLPto4b_tau1mm_M400_40_2018', '/mfv_HtoLLPto4b_tau1mm_M400_40_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_250_2018', '/mfv_HtoLLPto4b_tau1mm_M600_250_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1mm_M600_60_2018', '/mfv_HtoLLPto4b_tau1mm_M600_60_2018/None/USER', 24500),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_350_2018', '/mfv_HtoLLPto4b_tau1mm_M800_350_2018/None/USER', 25000),
MCSample('mfv_HtoLLPto4b_tau1mm_M800_80_2018', '/mfv_HtoLLPto4b_tau1mm_M800_80_2018/None/USER', 24500),
]

mfv_ZprimetoLLPto4j_samples_2016 = [
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2016/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2016/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2016/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2016/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2016/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2016', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2016/None/USER', 5000),
]

mfv_ZprimetoLLPto4j_samples_2017 = [
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017/None/USER', 5000),
]

mfv_ZprimetoLLPto4j_samples_2018 = [
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2018/None/USER', 4000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2018/None/USER', 4000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2018/None/USER', 4000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2018', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2018/None/USER', 3000),
]

mfv_ZprimetoLLPto4b_samples_2016 = [
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2016/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2016', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2016/None/USER', 5000),
]

mfv_ZprimetoLLPto4b_samples_2017 = [
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017/None/USER', 5000),
]

mfv_ZprimetoLLPto4b_samples_2018 = [
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2018/None/USER', 4500),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2018/None/USER', 5000),
MCSample('mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2018', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2018/None/USER', 5000),
]

for s in mfv_splitSUSY_samples_2016 + mfv_splitSUSY_samples_2017 + mfv_splitSUSY_samples_2018 + mfv_HtoLLPto4j_samples_2016 + mfv_HtoLLPto4j_samples_2017 + mfv_HtoLLPto4j_samples_2018 + mfv_HtoLLPto4b_samples_2016 + mfv_HtoLLPto4b_samples_2017 + mfv_HtoLLPto4b_samples_2018 + mfv_ZprimetoLLPto4j_samples_2016 + mfv_ZprimetoLLPto4j_samples_2017 + mfv_ZprimetoLLPto4j_samples_2018 + mfv_ZprimetoLLPto4b_samples_2016 + mfv_ZprimetoLLPto4b_samples_2017 + mfv_ZprimetoLLPto4b_samples_2018:
    #print "JOEY mass is %s" % _mass(s) # FIXME we're dropping the LSP mass; could do something custom here to only parse that part though...
    _set_signal_stuff(s)

########
# data
########

data_samples_2017 = [                                              # in dataset      in json          int lumi avail (/fb)
    DataSample('JetHT2017B', '/JetHT/Run2017B-17Nov2017-v1/AOD'),  # 297047 299329   297050 299329     4.794
    DataSample('JetHT2017C', '/JetHT/Run2017C-17Nov2017-v1/AOD'),  # 299368 302029   299368 302029     9.631
    DataSample('JetHT2017D', '/JetHT/Run2017D-17Nov2017-v1/AOD'),  # 302031 302663   302031 302663     4.248
    DataSample('JetHT2017E', '/JetHT/Run2017E-17Nov2017-v1/AOD'),  # 303824 304797   303825 304797     9.315
    DataSample('JetHT2017F', '/JetHT/Run2017F-17Nov2017-v1/AOD'),  # 305040 306460   305044 306460    13.540
    ]

auxiliary_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-17Nov2017-v1/AOD'),
    ]

data_samples_2018 = [
    DataSample('JetHT2018A', '/JetHT/Run2018A-17Sep2018-v1/AOD'),  # 315257 316995   315257 316995   14.028
    DataSample('JetHT2018B', '/JetHT/Run2018B-17Sep2018-v1/AOD'),  # 317080 319310   317080 319077    7.067
    DataSample('JetHT2018C', '/JetHT/Run2018C-17Sep2018-v1/AOD'),  # 319337 320065   319337 320065    6.895
    DataSample('JetHT2018D', '/JetHT/Run2018D-PromptReco-v2/AOD'), # 320497 325175   320673 325172   31.747
    ]

auxiliary_data_samples_2018 = [
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-17Sep2018-v2/AOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-17Sep2018-v1/AOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-17Sep2018-v1/AOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-PromptReco-v2/AOD'),
    ]

########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - can't add data by primary (have the same primary for different datasets)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

__all__ = [
    'qcd_samples_2017',
    'ttbar_samples_2017',
    'bjet_samples_2017',
    'bjet_samples_sum_2017',
    'leptonic_samples_2017',
    'leptonic_samples_sum_2017',
    'mfv_signal_samples_2017',
    'mfv_stopdbardbar_samples_2017',
    'qcd_samples_2018',
    'ttbar_samples_2018',
    'bjet_samples_2018',
    'mfv_signal_samples_2018',
    'mfv_stopdbardbar_samples_2018',
    'data_samples_2017',
    'auxiliary_data_samples_2017',
    'data_samples_2018',
    'auxiliary_data_samples_2018',
    'mfv_splitSUSY_samples_2016',
    'mfv_splitSUSY_samples_2017',
    'mfv_splitSUSY_samples_2018',
    'mfv_HtoLLPto4j_samples_2016',
    'mfv_HtoLLPto4j_samples_2017',
    'mfv_HtoLLPto4j_samples_2018',
    'mfv_HtoLLPto4b_samples_2016',
    'mfv_HtoLLPto4b_samples_2017',
    'mfv_HtoLLPto4b_samples_2018',
    'mfv_ZprimetoLLPto4j_samples_2016',
    'mfv_ZprimetoLLPto4j_samples_2017',
    'mfv_ZprimetoLLPto4j_samples_2018',
    'mfv_ZprimetoLLPto4b_samples_2016',
    'mfv_ZprimetoLLPto4b_samples_2017',
    'mfv_ZprimetoLLPto4b_samples_2018',

    'registry',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        registry.add_list(x,o)
        for sample in o:
            registry.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)

span_signal_samples_2017 = [eval('mfv_%s_tau%06ium_M%04i_2017' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (400,800,1600,3000)]
span_signal_samples_2018 = [eval('mfv_%s_tau%06ium_M%04i_2018' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (400,800,1600,3000)]

_alls = [
    'all_signal_samples_2017',
    'all_signal_samples_2018',
    'span_signal_samples_2017',
    'span_signal_samples_2018',
    ]
__all__ += _alls
for x in _alls:
    registry.add_list(x, eval(x))

########################################################################

########
# Extra datasets and other overrides go here.
########

########
# miniaod
########

## Setting up StealthSUSY
for sample in StealthSHH_samples_2017 + StealthSYY_samples_2017 + StealthSHH_samples_2018 + StealthSYY_samples_2018:
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)

StealthSHH_mStop_1100_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-3fc538f6a65ecefa0ce7ef02f4104ede/USER', 103501)
StealthSHH_mStop_1100_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-43231f4894e16e921d1ab28be7d00d3d/USER', 76384)
StealthSHH_mStop_1100_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-dc76e6a510dbcf533b5d196b85b2862b/USER', 87091)
StealthSHH_mStop_1100_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-5d6d8963b53a7af15ba972733d9a3fb5/USER', 86935)
StealthSHH_mStop_1100_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-594e97dfedd63104c54c988e9e4d9e22/USER', 77628)
StealthSHH_mStop_1100_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-b8c3cfa4e425a10403a160725e45fa05/USER', 73492)
StealthSHH_mStop_1100_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-3f5cf71b3d841c547122510989beba16/USER', 94191)
StealthSHH_mStop_1100_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-1b747427203d7867466fc5ea119bc033/USER', 92664)
StealthSHH_mStop_1100_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-0bf8a24d2969f5422cb6bc4d30c018a3/USER', 93610)
StealthSHH_mStop_1100_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-16b4ec51b5d0a3c17386e758b49849e4/USER', 80333)
StealthSHH_mStop_1100_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-03f1261b3f324153893c0493e683b938/USER', 90967)
StealthSHH_mStop_1100_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-3568a5c62f23ad0b52d1a874cb39ee13/USER', 88887)
StealthSHH_mStop_1100_mS_875_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-78a88757e91db259764498d28b7f229b/USER', 69640)
StealthSHH_mStop_1100_mS_875_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-219abeadfb2e6f02f98d3108dabb520a/USER', 88658)
StealthSHH_mStop_1100_mS_875_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2e60864b530ea584808c3647d45183ce/USER', 74456)
StealthSHH_mStop_1100_mS_875_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7a1a6c03cc002847f76f7fd9789bf10e/USER', 80666)
StealthSHH_mStop_1100_mS_875_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4fa6967a12c299eed3a82313a2c83207/USER', 71960)
StealthSHH_mStop_1100_mS_875_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-689d16c3becd1cb3c87f7e20c35c6f2d/USER', 84192)
StealthSHH_mStop_1100_mS_875_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-bec159b18583acdd89a7f0ea955a5893/USER', 77898)
StealthSHH_mStop_1100_mS_875_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-57309888707208d53d308f4fd74698e1/USER', 80482)
StealthSHH_mStop_1100_mS_875_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d1f6dd7618821cf20e53fcec38a7d066/USER', 73773)
StealthSHH_mStop_1100_mS_875_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-3bc7f9722a417098c9bffa0d16ea2bb1/USER', 86476)
StealthSHH_mStop_1100_mS_875_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8939d7aa2c9bf7a28ac2b3d623f6b7a6/USER', 78229)
StealthSHH_mStop_1100_mS_875_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a28f56470f60fda8164012793d9d54af/USER', 105430)
StealthSHH_mStop_1300_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ea29995cd6102d263e68380f99ec4a69/USER', 99893)
StealthSHH_mStop_1300_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-712af1f4bde5b1f39171381a047f8a8b/USER', 85137)
StealthSHH_mStop_1300_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d26b5080924e5553750ac09b36942260/USER', 81695)
StealthSHH_mStop_1300_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c3f04389ff91530b9828b58aae5f8a0b/USER', 80209)
StealthSHH_mStop_1300_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a6504f1ca8f61f0b8051122e51e4e132/USER', 85949)
StealthSHH_mStop_1300_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-92cfc66ff4b7b81db56b57d5f8a07521/USER', 74003)
StealthSHH_mStop_1300_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-f466b1a064c214901812e8d818f99245/USER', 90046)
StealthSHH_mStop_1300_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-0eab8da4508846c17f3edf081280b69a/USER', 78589)
StealthSHH_mStop_1300_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-30b330d258a4894af0f25cb426eaa56d/USER', 104488)
StealthSHH_mStop_1300_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a75d20f57a37dc226b9dd602b9d76a68/USER', 81973)
StealthSHH_mStop_1300_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ec24d8b877b05fa7fbad1264c2cbd15b/USER', 95451)
StealthSHH_mStop_1300_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-ae967e38383a4c245c8f52278e106ac2/USER', 84298)
StealthSHH_mStop_1300_mS_1075_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-89b4baa6e479f6f26e42fb2d02d6bf1b/USER', 96746)
StealthSHH_mStop_1300_mS_1075_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-93ba4b0199a589c6652df784112578ba/USER', 101120)
StealthSHH_mStop_1300_mS_1075_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1d17da0e2a8d5d9aaf4fab599e2f4b5c/USER', 108824)
StealthSHH_mStop_1300_mS_1075_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d2b896c87652a42dceacb469c0a64001/USER', 72138)
StealthSHH_mStop_1300_mS_1075_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-31c1f89269ca966668eab6d82354925e/USER', 84127)
StealthSHH_mStop_1300_mS_1075_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-6142d171385a24d7e3045639e1fb7e2f/USER', 75182)
StealthSHH_mStop_1300_mS_1075_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6a1a86e897cb1f13bd27f760f0d55378/USER', 91976)
StealthSHH_mStop_1300_mS_1075_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-119a57d212e12ca18d324f675a5e7682/USER', 75722)
StealthSHH_mStop_1300_mS_1075_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1c6174d99bed5e848109dd595b9e74fd/USER', 87150)
StealthSHH_mStop_1300_mS_1075_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-01d7c4c279a124ba74d1a1c29dc84d49/USER', 96922)
StealthSHH_mStop_1300_mS_1075_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4653e76ba3bb0d195d0c89ce4e916b9f/USER', 83883)
StealthSHH_mStop_1300_mS_1075_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-0ce6f91224952b837d0c12948a425b3f/USER', 83970)
StealthSHH_mStop_1500_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d14067123781fcb9fb8f01af4bfb1356/USER', 95490)
StealthSHH_mStop_1500_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-ee2ea1cffe9875532f8a5de9ed08153a/USER', 72552)
StealthSHH_mStop_1500_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-17434cdb13d7c7ef071dec5e16d709da/USER', 108739)
StealthSHH_mStop_1500_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-bde1979bfe559c1aad9d2f3e8bde64d8/USER', 91034)
StealthSHH_mStop_1500_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e20095712b6e048567e0d47cd0bbb293/USER', 90288)
StealthSHH_mStop_1500_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7c648ba700cb065eafb15e053bd3c1f2/USER', 99179)
StealthSHH_mStop_1500_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-532ee3ca92bbc3ceb6da40fb827748b1/USER', 99451)
StealthSHH_mStop_1500_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-e611e225907bca69236d7c28f6695439/USER', 87798)
StealthSHH_mStop_1500_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d1c5da6ce2be5964536f7afc8b46e360/USER', 90783)
StealthSHH_mStop_1500_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fb7dd729f7a6b80b3edd5e48d1e1e5b6/USER', 80785)
StealthSHH_mStop_1500_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9127a7e3144264204c504de7ca3260d7/USER', 103226)
StealthSHH_mStop_1500_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-50a4a00d03f6b26e19c613e8b489f14f/USER', 83185)
StealthSHH_mStop_1500_mS_1275_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8d17f6e669564ba52bdda13ac2eca192/USER', 94151)
StealthSHH_mStop_1500_mS_1275_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c1f27eaa17d281bb8b4f0a1bb584a7be/USER', 92525)
StealthSHH_mStop_1500_mS_1275_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4731263c354c3bf591291c855533b1df/USER', 89495)
StealthSHH_mStop_1500_mS_1275_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9f9683ed29a1531b2c6817ef854c2051/USER', 90609)
StealthSHH_mStop_1500_mS_1275_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-81e88b0bcc6b433b5acf1e67c4792669/USER', 92697)
StealthSHH_mStop_1500_mS_1275_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-e6529252319bda02a79135a515c52010/USER', 92323)
StealthSHH_mStop_1500_mS_1275_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6f3fc8c120f6f55d2ed80fe87b384d70/USER', 89330)
StealthSHH_mStop_1500_mS_1275_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-b0b0710ae365a8cbd495ca82ac661ffb/USER', 79352)
StealthSHH_mStop_1500_mS_1275_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-f94e229f9dfd28c67d115a1df6611707/USER', 79265)
StealthSHH_mStop_1500_mS_1275_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d88d330d69f9ed82a45f83f8a72c6f55/USER', 96939)
StealthSHH_mStop_1500_mS_1275_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-21c925eaf0e6716d7f4962a03b6b7b7b/USER', 82203)
StealthSHH_mStop_1500_mS_1275_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-53741756c4cd69dfd8f9de4db395e8b6/USER', 83229)
StealthSHH_mStop_300_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-5f136299f426ca8fd786e289a7ca12ed/USER', 41541)
StealthSHH_mStop_300_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d914dd092e77afc0b521a1b63a6cd470/USER', 42157)
StealthSHH_mStop_300_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c94f380f4738bf4f7586267f84a7b8ae/USER', 48629)
StealthSHH_mStop_300_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c6ccb26eae2c943ce27a3721e0a07b7f/USER', 51544)
StealthSHH_mStop_300_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9943e8eb7bcd324fd0691368623fc832/USER', 30510)
StealthSHH_mStop_300_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7a62630b41d2931331e399c3504e92b2/USER', 39373)
StealthSHH_mStop_300_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-22892c3af83ac1100397c11e0f28593b/USER', 45156)
StealthSHH_mStop_300_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-bedd68bbd25c53a61c8e42dddea555e1/USER', 35532)
StealthSHH_mStop_300_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-87e405795ce3b5f158ed24ca688e9839/USER', 46670)
StealthSHH_mStop_300_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-049d49f8017050fdbb6aa638e9924def/USER', 38084)
StealthSHH_mStop_300_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-07835c1c6617865fd9e28c944fe0be1d/USER', 43788)
StealthSHH_mStop_300_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-821cb8472fcbd4a8b3303d7b30c2ed49/USER', 46009)
StealthSHH_mStop_300_mS_75_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-cb5910bdde39c11c503fe935f093fa84/USER', 41030)
StealthSHH_mStop_300_mS_75_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-cc55d7960fe8f4bb9ef3bb07ef53bedd/USER', 34341)
StealthSHH_mStop_300_mS_75_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2a39961916520d9731ec6a89d58a4e9c/USER', 39905)
StealthSHH_mStop_300_mS_75_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-5901a1d08d91a4199ee7ed4fb58ea22d/USER', 41387)
StealthSHH_mStop_300_mS_75_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1abb577b159a4dfd65c6b24ea26c9b0f/USER', 36333)
StealthSHH_mStop_300_mS_75_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-264b4d1ab7badd9a0c4523ba793578c1/USER', 35820)
StealthSHH_mStop_300_mS_75_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6a622344c0df9e7a94f8d6d0f91f183e/USER', 40618)
StealthSHH_mStop_300_mS_75_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-1593e65ce627aa41cd2967a7ee6b2c69/USER', 37335)
StealthSHH_mStop_300_mS_75_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-83fda47d9a5dc918980f662e31e56bef/USER', 37946)
StealthSHH_mStop_300_mS_75_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-ee6b892b9194786cc7fea6f8b679afcf/USER', 36482)
StealthSHH_mStop_300_mS_75_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c35707b80f220d1b4e2dbc6dc0269d22/USER', 35843)
StealthSHH_mStop_300_mS_75_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-6cf582ba325a9c233227f51b4e425f75/USER', 36965)
StealthSHH_mStop_500_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-045b8060ae21fa6c24d8d1a3d4738a1a/USER', 75405)
StealthSHH_mStop_500_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a151c0856f350428f46f4a9412171821/USER', 70649)
StealthSHH_mStop_500_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-401ce2bd8e3bc403613bcae912cf9bba/USER', 51804)
StealthSHH_mStop_500_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-795f3cf6c8b4a898a91fb1582c2c8a7f/USER', 64271)
StealthSHH_mStop_500_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-abb94e2016f152bd81e50d2c8f3d4fac/USER', 54952)
StealthSHH_mStop_500_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d29e6a34b96b5ae4cf283ebda318bee8/USER', 45584)
StealthSHH_mStop_500_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-7e19c54c66dafbdd4d6d80eca9ae65d6/USER', 69617)
StealthSHH_mStop_500_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-94ae4ae6d87a0408b03b46622bafabd7/USER', 62926)
StealthSHH_mStop_500_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-7aa155180ef02a34985acdf75f7567b7/USER', 62037)
StealthSHH_mStop_500_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d521a07493840355db975eeab20ce727/USER', 69955)
StealthSHH_mStop_500_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9a1366d2dddcf21e385fcaf398b1d289/USER', 75955)
StealthSHH_mStop_500_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-665ab7b0e2d64a4f911cf139e88a9b50/USER', 68223)
StealthSHH_mStop_500_mS_275_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6a3bc82a14d01510af03cdf9eea59dd0/USER', 53574)
StealthSHH_mStop_500_mS_275_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-64f3efba0c0dc070a3d0ca8356eed52e/USER', 48545)
StealthSHH_mStop_500_mS_275_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2955560d6fa31446e119ace8b4cea72b/USER', 54593)
StealthSHH_mStop_500_mS_275_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7ebd4bd27f83fb80aeea00ed6ee0bd5c/USER', 62285)
StealthSHH_mStop_500_mS_275_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2aaeffcc5f8235f47eb18cf40a56fffa/USER', 45700)
StealthSHH_mStop_500_mS_275_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-aafde422b80d75552c4a38cd798a54d2/USER', 42352)
StealthSHH_mStop_500_mS_275_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6de62c84023c96ff8b8e9add3a801a7f/USER', 47610)
StealthSHH_mStop_500_mS_275_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-6fc850c842e585f4bb2d7d6349a08c40/USER', 65784)
StealthSHH_mStop_500_mS_275_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-401200bd21c49d469e169373fefbfcef/USER', 57329)
StealthSHH_mStop_500_mS_275_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-5029d328092d82d3094b3794a7c45122/USER', 49793)
StealthSHH_mStop_500_mS_275_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8ea96a5421b72dd5af9e31fbb91452a3/USER', 57138)
StealthSHH_mStop_500_mS_275_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-ba84ab41da807d3f7ab1a6d998de8d5e/USER', 57090)
StealthSHH_mStop_700_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-34222ae17b2a15a183633cb1f0842941/USER', 93401)
StealthSHH_mStop_700_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-30c8702728508c7206328862859cd9b5/USER', 78366)
StealthSHH_mStop_700_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-72b74a2471cc776a83d10e33d3ec596f/USER', 78758)
StealthSHH_mStop_700_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-10867a2c8abbbe4dd02ff1fc8a07cde8/USER', 90915)
StealthSHH_mStop_700_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-47835fa8f85717d5c3c5ab1dbe480190/USER', 62403)
StealthSHH_mStop_700_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2a12d8a7b77762778ea7404da26c7ba8/USER', 71384)
StealthSHH_mStop_700_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-7b12f1e8cd0e98eb64c24368c6f29da3/USER', 90873)
StealthSHH_mStop_700_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-78b67ea7c29284081d43f5e34e4e0f8d/USER', 81556)
StealthSHH_mStop_700_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-386e06d8fea3be6d47812bacf10ab9ab/USER', 86424)
StealthSHH_mStop_700_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-5fe29b9c2447218ffcdb37d9d738c452/USER', 82050)
StealthSHH_mStop_700_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-26ba998a66e0e3c8b56b85cdb9ceccb7/USER', 74492)
StealthSHH_mStop_700_mS_475_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ee996066021d73bc8b95e5526e000837/USER', 66387)
StealthSHH_mStop_700_mS_475_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-029d94d2b1a8751ea1d2d19e5a489b2a/USER', 63388)
StealthSHH_mStop_700_mS_475_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c537e860f6f67f2af86189d22f893a85/USER', 59259)
StealthSHH_mStop_700_mS_475_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9790b66608a23674411310bd1f4819b1/USER', 60338)
StealthSHH_mStop_700_mS_475_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e336268a0f30cfad1cff06b28a7e5a30/USER', 53787)
StealthSHH_mStop_700_mS_475_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-8368aed649b244bc493815f4151edd58/USER', 51623)
StealthSHH_mStop_700_mS_475_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-99d4b0fb671a568c3a353bec594b6e7f/USER', 70121)
StealthSHH_mStop_700_mS_475_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-8f7f9de87895492cf5d7d39f6e036b42/USER', 54383)
StealthSHH_mStop_700_mS_475_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ca9d2fbc9e7707f24cfce31132e9e9db/USER', 68090)
StealthSHH_mStop_700_mS_475_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f9f5f8175b7c15a7b1eeccdc4ff26793/USER', 66276)
StealthSHH_mStop_700_mS_475_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-b75637ded063511d3db45579d6da49ed/USER', 57746)
StealthSHH_mStop_700_mS_475_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-8160a2b3eed9057195e78b40176ea507/USER', 77237)
StealthSHH_mStop_900_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-759d04852d1bd624d696a229b44336ab/USER', 103373)
StealthSHH_mStop_900_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-bac3b473b23329bb7ce235d03e7c0e05/USER', 99662)
StealthSHH_mStop_900_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-142891bf388b8612300ff4b6f2d9cdf6/USER', 93750)
StealthSHH_mStop_900_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2336af8a2c0d621575369f68894ead2c/USER', 104782)
StealthSHH_mStop_900_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-05b691f126b7f7b5fb30c7e85d4a7134/USER', 73201)
StealthSHH_mStop_900_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f583424543f6f56f0bc8e34c7802de92/USER', 94392)
StealthSHH_mStop_900_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4166fb83ae8497a097dc4e22e558dd6d/USER', 108595)
StealthSHH_mStop_900_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-51c41c017faf1858f1dcc89e43a2fe46/USER', 97340)
StealthSHH_mStop_900_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8abaec81c2b683a0a1cbe906c203e946/USER', 95163)
StealthSHH_mStop_900_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f49b3d8ff2381107a05972d02b9e5157/USER', 103844)
StealthSHH_mStop_900_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-fa4d174f44da16e81cae02424362a98d/USER', 96819)
StealthSHH_mStop_900_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-5cd628314d7fb582ca7850100388b109/USER', 78933)
StealthSHH_mStop_900_mS_675_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-67ca1cd33636027775fd974bf8e61012/USER', 84744)
StealthSHH_mStop_900_mS_675_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-71b7b7e4dd204826b0be2ff2ed10f9eb/USER', 84073)
StealthSHH_mStop_900_mS_675_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6247691bb936c12890e89b09e2d24d60/USER', 77060)
StealthSHH_mStop_900_mS_675_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f57faefc220e66517863a5b4310e7182/USER', 77392)
StealthSHH_mStop_900_mS_675_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1a75189d36b23b46188f6c7fb6b5432d/USER', 56498)
StealthSHH_mStop_900_mS_675_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f8c33a00b2fa5a55088c4b8ab54dc195/USER', 57450)
StealthSHH_mStop_900_mS_675_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d72189bea0539645ae1565ac333842d7/USER', 66985)
StealthSHH_mStop_900_mS_675_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7288d463366524d9f8513365f112acc7/USER', 65948)
StealthSHH_mStop_900_mS_675_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-34de66f43a93d3f40bb3020a3df98600/USER', 69529)
StealthSHH_mStop_900_mS_675_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c834da920cdb8ec7353232d98fc5022d/USER', 76358)
StealthSHH_mStop_900_mS_675_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-300e31200177dfa1af340b3002a72d7e/USER', 80439)
StealthSHH_mStop_900_mS_675_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSHH_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-b709baca860e29f5ff0b627f3180c660/USER', 76453)
StealthSYY_mStop_1100_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d5e8ce2456fb4ddfe54c9e97f76c98a1/USER', 81142)
StealthSYY_mStop_1100_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fa8e2c48715367194d56b77fc4cee3db/USER', 98618)
StealthSYY_mStop_1100_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-67a8357e135c497863926d3a5bd27f60/USER', 111921)
StealthSYY_mStop_1100_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a385e9591205cabf48e95e4d785fb8bd/USER', 101579)
StealthSYY_mStop_1100_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e5755723326c5528c72c2821d7d710a7/USER', 90321)
StealthSYY_mStop_1100_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-ef8d8859ac46272f6eb000f6e767e16a/USER', 91823)
StealthSYY_mStop_1100_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-0aa816c411156d3fd3a490199d7692ad/USER', 109599)
StealthSYY_mStop_1100_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-5046f4a7037bd5afd9d6ec82054a0f29/USER', 93674)
StealthSYY_mStop_1100_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c2dafe4b6ad6fd228604b4fbacc4fd0e/USER', 82958)
StealthSYY_mStop_1100_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-89c906e4d5b9c40f3978549048010eec/USER', 85606)
StealthSYY_mStop_1100_mS_875_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ca6609a32e4643573cae90f285c7bdfe/USER', 62318)
StealthSYY_mStop_1100_mS_875_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-23d02f8370a9ca4dc837de9c8b63e06d/USER', 86268)
StealthSYY_mStop_1100_mS_875_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e3b6f3c74926f0fe3806b0c1519f1222/USER', 53300)
StealthSYY_mStop_1100_mS_875_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-41d3989b45c20ff706f45747dd6ee3c2/USER', 87649)
StealthSYY_mStop_1100_mS_875_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-57c73b5706adec263be308f703ee0a33/USER', 67505)
StealthSYY_mStop_1100_mS_875_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-50a62bc27f8c3589450781aae14f8143/USER', 73508)
StealthSYY_mStop_1100_mS_875_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9cdeb207650baa032ea9ee5f599c78e8/USER', 63943)
StealthSYY_mStop_1100_mS_875_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-841ad6e06557fc1489edd33f9a33cb86/USER', 93079)
StealthSYY_mStop_1100_mS_875_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c8f080989982d4bb57c8ba6cca5f1e07/USER', 75578)
StealthSYY_mStop_1100_mS_875_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d5a09997883574a0c1374b56034c35ae/USER', 79005)
StealthSYY_mStop_1100_mS_875_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-30173f78cea83de2abc054c90b113f16/USER', 73369)
StealthSYY_mStop_1100_mS_875_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-e9daba0e0cf11de0770008e78d241a34/USER', 76201)
StealthSYY_mStop_1300_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-5830b8ba381c598a4740b2efb8442e03/USER', 100254)
StealthSYY_mStop_1300_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-45a9f44f6ac9152b0908a45be5417ea6/USER', 101715)
StealthSYY_mStop_1300_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2b76411c6c9defb8c5598969175b64d1/USER', 92047)
StealthSYY_mStop_1300_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-4961877da343cdda05f869ffeb721f66/USER', 104989)
StealthSYY_mStop_1300_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8023576bbc3a5fa061bb5e18de57b2e9/USER', 105884)
StealthSYY_mStop_1300_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-def65ea3a03160508f9ae9d5d9a6f8a5/USER', 101822)
StealthSYY_mStop_1300_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-89b056452a2c941c2fb94ca6918eee86/USER', 84582)
StealthSYY_mStop_1300_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9db8effe8906fa82c790232ac7545e59/USER', 85306)
StealthSYY_mStop_1300_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-b5fc1f2044ff0090af48e3a7cacdd5df/USER', 84275)
StealthSYY_mStop_1300_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d30ed70ea2f78e30de7d070a3cdb9fe7/USER', 110372)
StealthSYY_mStop_1300_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8c823a80a66e813bef644e28c4660c5c/USER', 73397)
StealthSYY_mStop_1300_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9ca6e6c8bbe20bbde87ddc6fb2a711da/USER', 107731)
StealthSYY_mStop_1300_mS_1075_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-dc0b5f906956f955a6ed7f0e5b9354dc/USER', 87690)
StealthSYY_mStop_1300_mS_1075_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-bb3e4515083f5ebccafd4998bb5c1372/USER', 97088)
StealthSYY_mStop_1300_mS_1075_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-611037990f945769848b0bf0da008b91/USER', 73010)
StealthSYY_mStop_1300_mS_1075_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-40b56a66e736662bb8b08207afa73713/USER', 91220)
StealthSYY_mStop_1300_mS_1075_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-692cc04b02c4ff1058fe6a5f19755eb1/USER', 61834)
StealthSYY_mStop_1300_mS_1075_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-28f29ae7dc43847adfbf533d60d57db3/USER', 87714)
StealthSYY_mStop_1300_mS_1075_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-76f927d2e20d00498435222469487571/USER', 82324)
StealthSYY_mStop_1300_mS_1075_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-65c85cf0fff76efd9c87f0630f9b35c5/USER', 79044)
StealthSYY_mStop_1300_mS_1075_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-56a48dae8760fea934338aecc2c1f617/USER', 77306)
StealthSYY_mStop_1300_mS_1075_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c0474ce23bb8b91dbec69c8dc3271159/USER', 89391)
StealthSYY_mStop_1300_mS_1075_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2ead7e33074d698edc17b62d8daa87eb/USER', 98728)
StealthSYY_mStop_1500_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-0d3b27245d225704cad76e6291ab5c70/USER', 78070)
StealthSYY_mStop_1500_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-184554b77d20a943030ff7c70c24ab2b/USER', 122828)
StealthSYY_mStop_1500_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6a665e0dcd42b45fb3ad8a4f648a0ae2/USER', 90802)
StealthSYY_mStop_1500_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d570878d0faf0d52569f1aa42fea87c4/USER', 101565)
StealthSYY_mStop_1500_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-02c0f2b5aedd9c4264559750952440ed/USER', 85915)
StealthSYY_mStop_1500_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-434b71cb4e0071057d72e932b5eb86bc/USER', 105211)
StealthSYY_mStop_1500_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1c77027c0891319016b1209f80d26b7e/USER', 104806)
StealthSYY_mStop_1500_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-3d97821cc3e6d76d562c0f95ef2df536/USER', 90351)
StealthSYY_mStop_1500_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a89ef1b11e469ab22013d393480d92e9/USER', 74068)
StealthSYY_mStop_1500_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9a21bf284f5d24f57cd4686e287d7ac7/USER', 94859)
StealthSYY_mStop_1500_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-fa015fd660c65aeebfd47caf4a5bcaf9/USER', 85219)
StealthSYY_mStop_1500_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2f44da997b933dd3702b3344d8f5bbd6/USER', 95279)
StealthSYY_mStop_1500_mS_1275_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4e388139bee33fc819f2e4bac7ee86bf/USER', 87636)
StealthSYY_mStop_1500_mS_1275_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-175a09bd2e9cb1419ac298a969f2e4fe/USER', 95035)
StealthSYY_mStop_1500_mS_1275_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6eb2ba68fac68a5d4321b9cdf4fa7efb/USER', 89789)
StealthSYY_mStop_1500_mS_1275_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fea36a96bea91e6602ca2bda966b6ad1/USER', 102462)
StealthSYY_mStop_1500_mS_1275_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-663fbb1d75bf69363ba2e81a13e5d1c9/USER', 87629)
StealthSYY_mStop_1500_mS_1275_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-71914c16279033e3b864ae9e6cf70d41/USER', 89974)
StealthSYY_mStop_1500_mS_1275_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-aa0658372cd1a4a9a947a827e62edacb/USER', 77872)
StealthSYY_mStop_1500_mS_1275_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-87ac03a011b8163ea7c090e300bbb301/USER', 96297)
StealthSYY_mStop_1500_mS_1275_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-fa5ba1235fcbeebf9c3e9948397a06bd/USER', 82881)
StealthSYY_mStop_1500_mS_1275_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-9bc02c13c3979aaff4035f3c00b45835/USER', 84669)
StealthSYY_mStop_1500_mS_1275_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-426d168eb244a84173e77ea8deeefad5/USER', 101665)
StealthSYY_mStop_1500_mS_1275_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-b25de2b465163240e7168daf5dfcdb23/USER', 90656)
StealthSYY_mStop_300_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-295902482332ffeefa162e9b5b48d591/USER', 30666)
StealthSYY_mStop_300_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fa6d91a2e2b55a6ec08c8d23ed1d62a3/USER', 38411)
StealthSYY_mStop_300_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1765b4f86fb28d3e5f4e1a56cfe63944/USER', 41263)
StealthSYY_mStop_300_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a028b6367ae5e982531f64881707f314/USER', 35980)
StealthSYY_mStop_300_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-dc775099fe04955d8a50617047a21246/USER', 44481)
StealthSYY_mStop_300_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-20313ab5e177751172a26a49d0cc9076/USER', 39695)
StealthSYY_mStop_300_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4968806879b592574c65f2a0c28b3161/USER', 31601)
StealthSYY_mStop_300_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c3b2594f96d95179164723ae3ec153e8/USER', 36673)
StealthSYY_mStop_300_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8e087581556e8c92aef208d343f84f20/USER', 35710)
StealthSYY_mStop_300_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-0121fefb83940331c47ea9ac33ecf657/USER', 38316)
StealthSYY_mStop_300_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e3889e25d74a50e8cdf31e0f84c6801a/USER', 38877)
StealthSYY_mStop_300_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-784593942ccce724579914a2bedcb81f/USER', 41305)
StealthSYY_mStop_300_mS_75_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4dadae9131936d49bec2f02f4aa5cca1/USER', 30543)
StealthSYY_mStop_300_mS_75_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-13533bf48c6e2d8ae9bc514a9a9358a6/USER', 36894)
StealthSYY_mStop_300_mS_75_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-10bf953d547aa76716f2995548d84586/USER', 35175)
StealthSYY_mStop_300_mS_75_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-95c494e090a9641c05891f384cf34b78/USER', 35674)
StealthSYY_mStop_300_mS_75_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-b5c432f286d761728a3d68ec9f669e9b/USER', 37384)
StealthSYY_mStop_300_mS_75_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-cdd1671e432700137bbc5a0ee7f07ba2/USER', 34208)
StealthSYY_mStop_300_mS_75_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-eeacb8406f87a2df3fc14c758c7167e7/USER', 38876)
StealthSYY_mStop_300_mS_75_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c6ff223a1344cad2e237d8f25d81db1a/USER', 34226)
StealthSYY_mStop_300_mS_75_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a3499810b318c788dc806553d2742911/USER', 36612)
StealthSYY_mStop_300_mS_75_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-8d2d4b86f68659c9bc63b61516d27a74/USER', 37607)
StealthSYY_mStop_300_mS_75_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e3554ee588cbaeb75094668dab047835/USER', 36626)
StealthSYY_mStop_300_mS_75_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a347247c04b9bda5d6a7a2e0a5a06d5b/USER', 37124)
StealthSYY_mStop_500_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-f9e154160908ee2462b9ea7095affe2b/USER', 49105)
StealthSYY_mStop_500_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-0b9abe56c2675d9da40564b87dd13225/USER', 67026)
StealthSYY_mStop_500_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-f36747913fbeb756b5d73020d9ad1b57/USER', 61194)
StealthSYY_mStop_500_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-b4f5d0922df5ba641aec556a761a7af4/USER', 68569)
StealthSYY_mStop_500_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-ec2c86948a63da596c4bb380fd2fce3c/USER', 53863)
StealthSYY_mStop_500_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-df7dfca3d61e29ecb0d3b671edde34e6/USER', 55621)
StealthSYY_mStop_500_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a8f53d2e9474ccd535759088c113acf3/USER', 40642)
StealthSYY_mStop_500_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2816135da12bbfb969c84fb4b2a6078a/USER', 45273)
StealthSYY_mStop_500_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-57f779d22e7dea6a290e7333962152f6/USER', 60037)
StealthSYY_mStop_500_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d280ac9ffe1d2ade4705b238f7b9c7fc/USER', 52863)
StealthSYY_mStop_500_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-1ea953c5124c66e4d27d213dc979a440/USER', 51856)
StealthSYY_mStop_500_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-afb905eecc678551cb602bd43de367d2/USER', 55187)
StealthSYY_mStop_500_mS_275_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-8d122c5211c95c4c454d8479311d1c47/USER', 40326)
StealthSYY_mStop_500_mS_275_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-726b3580b7929c642cffe06dc67cf654/USER', 47334)
StealthSYY_mStop_500_mS_275_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-cc72b897776112b3a921763c02690a39/USER', 42651)
StealthSYY_mStop_500_mS_275_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a9b108c4c9c28bd0219ad2cbee4f2a58/USER', 47119)
StealthSYY_mStop_500_mS_275_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-2196bdcb902510ff0fe8d8d9ad435a56/USER', 40741)
StealthSYY_mStop_500_mS_275_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-62eaea2091cdd95553c591cb1dfdb10d/USER', 41461)
StealthSYY_mStop_500_mS_275_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9e8f22baed720a75acc7facc736c127c/USER', 39770)
StealthSYY_mStop_500_mS_275_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f178a3d8d3cb5a8a2b28e71bab1d5de8/USER', 42367)
StealthSYY_mStop_500_mS_275_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a4e14f73fdb184cdd05eeb1bb8f14e9c/USER', 44201)
StealthSYY_mStop_500_mS_275_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-67ef6507131a6b8935a4d60421e6f4bc/USER', 46024)
StealthSYY_mStop_500_mS_275_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-c365275a552f23da0c00bdf6c78dc30a/USER', 43582)
StealthSYY_mStop_500_mS_275_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d9f7f5bed03867c8563d4f49951cf718/USER', 43125)
StealthSYY_mStop_700_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-04cfa66a5b1ea20a96f71f0da60b4293/USER', 77268)
StealthSYY_mStop_700_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-003f44425a0df192ba7bb562a757dff9/USER', 90855)
StealthSYY_mStop_700_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-9be17fd2911b0b7d9d068562b19704d9/USER', 86123)
StealthSYY_mStop_700_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-1f9daf983ffeb12653ab7e6f73a914cb/USER', 79344)
StealthSYY_mStop_700_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-03b9c4bc55bc163d997ebc5c600d47a1/USER', 83287)
StealthSYY_mStop_700_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-432452ef13a67132a9d313fb30a6229c/USER', 74273)
StealthSYY_mStop_700_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a749d98b7d3cf6915154e9e85e3ec397/USER', 65439)
StealthSYY_mStop_700_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-feea049567724b62782c67e551d107e8/USER', 88177)
StealthSYY_mStop_700_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4dfee6ed44a1b21320f1af440a2e480c/USER', 75905)
StealthSYY_mStop_700_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-7d35cef4484d611ad26cb12d68bac7c0/USER', 76345)
StealthSYY_mStop_700_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-aa9d28ce411ec041c8526defb5702f8a/USER', 84522)
StealthSYY_mStop_700_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-90c8789a95226836fd9900c06a636fed/USER', 90410)
StealthSYY_mStop_700_mS_475_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-aa253a5538b4ffebfbe12f47ee2c0b37/USER', 52936)
StealthSYY_mStop_700_mS_475_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-6f1362822de54bf8a64c9b2f992bb71c/USER', 49826)
StealthSYY_mStop_700_mS_475_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-deb6ca7a36fa296d79972f9754a712b3/USER', 54006)
StealthSYY_mStop_700_mS_475_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-4fefe77a999e1b944c0a3ed41c2d8b58/USER', 51941)
StealthSYY_mStop_700_mS_475_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-3842095fc84590c8eb6f39890067c585/USER', 45821)
StealthSYY_mStop_700_mS_475_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-d882c92fa0a8369fa89d7985d5cfdef5/USER', 46125)
StealthSYY_mStop_700_mS_475_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6845800a7c7098db966c35c2c65941e5/USER', 48655)
StealthSYY_mStop_700_mS_475_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-685ff7d271affbf1778e790ea38cefe1/USER', 64014)
StealthSYY_mStop_700_mS_475_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-0d092b436a469f56e149779c36d48ae8/USER', 59169)
StealthSYY_mStop_700_mS_475_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f8da88e26e9f8c846b13c267af9650ec/USER', 51829)
StealthSYY_mStop_700_mS_475_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-e643d1aeb78ee475471047a425636456/USER', 50596)
StealthSYY_mStop_700_mS_475_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-68ce22464ffd11a09637a3f2c38b5ab1/USER', 64390)
StealthSYY_mStop_900_mS_100_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-4089a1d8d1dc45d0ad84438307dc2add/USER', 82603)
StealthSYY_mStop_900_mS_100_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-0f5c36a751d4e19326fb7fedd7a71298/USER', 97881)
StealthSYY_mStop_900_mS_100_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-d6d0348c8129a051586e6188bd5fa363/USER', 97343)
StealthSYY_mStop_900_mS_100_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fba37a5deb0b44c2002fcaed61501d2a/USER', 88291)
StealthSYY_mStop_900_mS_100_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-5c3546549cdb90a3ade18ed223cbb78b/USER', 75762)
StealthSYY_mStop_900_mS_100_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-bb7045626c1aa09fb27b9d34de18c0be/USER', 89729)
StealthSYY_mStop_900_mS_100_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-3acf88cade7b50826bc6e15916f6cf61/USER', 94136)
StealthSYY_mStop_900_mS_100_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-71029d1a988e793733ffa3c5a9fb16dd/USER', 84126)
StealthSYY_mStop_900_mS_100_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-32f525839e5d9eaccf0054c1cd7126e0/USER', 87083)
StealthSYY_mStop_900_mS_100_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-04d07e11f9bb01205cf6cbdf071cd0ee/USER', 86335)
StealthSYY_mStop_900_mS_100_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-6878d232f142c37951f33d0660ca638a/USER', 91811)
StealthSYY_mStop_900_mS_100_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-a28d41e904c7f7c6dfa1f26fe0154379/USER', 107084)
StealthSYY_mStop_900_mS_675_ctau_0p01_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-7d810c2e4a11182313cfce63c7b29edd/USER', 59499)
StealthSYY_mStop_900_mS_675_ctau_0p01_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-44d62351d7f3ee3d394579c990cec9d9/USER', 80210)
StealthSYY_mStop_900_mS_675_ctau_0p1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-a34b8d887b25735765722c8155602604/USER', 66867)
StealthSYY_mStop_900_mS_675_ctau_0p1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-fbb93b0158cb230617c48e1fd4ca8474/USER', 64199)
StealthSYY_mStop_900_mS_675_ctau_1000_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-42df6166b31f286e514617305d388d23/USER', 51684)
StealthSYY_mStop_900_mS_675_ctau_1000_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-c7e826dd6873b629aac10a56a6048f68/USER', 55828)
StealthSYY_mStop_900_mS_675_ctau_100_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-3f5bb62c253ade1e5e7efe849b6b43b4/USER', 45597)
StealthSYY_mStop_900_mS_675_ctau_100_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-f374e6316ebb8218ca7ad2692b3bc930/USER', 60418)
StealthSYY_mStop_900_mS_675_ctau_10_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-32bdeb7190f7aacffbbd2a3758196416/USER', 61106)
StealthSYY_mStop_900_mS_675_ctau_10_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-2bb099d7c6f97ba2d75dc3a6ca69a8ba/USER', 51756)
StealthSYY_mStop_900_mS_675_ctau_1_2017.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV-madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2017-0c80426ed42fb218a15e95a6d738cdcd/USER', 62339)
StealthSYY_mStop_900_mS_675_ctau_1_2018.add_dataset('ntuplev27darksectorreviewm', '/StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_TuneCP5_13TeV_madgraphMLM-pythia8/brlopesd-ntuplev27darksectorreviewm_withGenInfom_2018-682cf7db2cf8eda670c72b51dc9bef05/USER', 67446)


for sample in data_samples_2017 + auxiliary_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset.replace('17Nov2017-v1/AOD', '31Mar2018-v1/MINIAOD'))
for sample in data_samples_2018 + auxiliary_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

_adbp('miniaod', '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',   59569132)
_adbp('miniaod', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',           56207744)
_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',          47724800)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 16882838)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',         11634434)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',           5941306)
ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',      154280331)
ttbarht0600_2017.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',    81507662)
ttbarht0800_2017.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',   40191637)
ttbarht1200_2017.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  13214871)
ttbarht2500_2017.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',    5155687)
wjetstolnu_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 33073306)
wjetstolnuext_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM', 44767978)
dyjetstollM10_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 39521230)
#dyjetstollM10ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 39536839)
dyjetstollM50_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 48675378)
dyjetstollM50ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561)
ttHbb_2017.add_dataset('miniaod', '/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 10055168)
ttZ_2017.add_dataset('miniaod', '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 9698473)
ttZext_2017.add_dataset('miniaod', '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM', 8536618)
singletop_tchan_top_2017.add_dataset('miniaod', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 5982064)
singletop_tchan_antitop_2017.add_dataset('miniaod', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 3675910)

_adbp('miniaod', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  21799788)
#_adbp('miniaod', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  11215220)
#_adbp('miniaod', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  11212810)
#_adbp('miniaod', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  14766010)
#_adbp('miniaod', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  10477146)
#_adbp('miniaod', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9104852)
#_adbp('miniaod', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',  8515107)
#_adbp('miniaod', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  2874295)
#_adbp('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',  5678761)
#_adbp('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  16073047)
#_adbp('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  15999466)
#_adbp('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9847660)
#_adbp('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9996886)
# the 2018 samples have 'MLM' in them so this works still, ugh
_adbp('miniaod', '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   54661579)
_adbp('miniaod', '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   55152960)
_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  43523821)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 15065049)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10955087)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   5475677)
ttbar_2018.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM', 142155064)
ttbarht0600_2018.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  14149394)
ttbarht0800_2018.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10372802)
ttbarht1200_2018.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 2779427)
ttbarht2500_2018.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  1451104)

_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99997)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99999)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 95000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99998)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 88000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)

_adbp('miniaod', '/mfv_splitSUSY_tau000000100um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2400_100_2016/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000000100um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000000100um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2400_100_2018/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2400_100_2018/None/USER', 10000)

_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_80_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_250_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_250_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_80_2016/None/USER', 25000),

_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_350_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_80_2017/None/USER', 25000),


_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_150_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_250_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau0p1mm_M800_80_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_150_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_250_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10000mm_M800_80_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_150_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M400_40_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M600_60_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1000mm_M800_80_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_150_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau100mm_M800_80_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_150_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M400_40_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau10mm_M800_80_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_150_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4j_tau1mm_M800_80_2018/None/USER', 25000),

_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_80_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_150_2016/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_80_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_150_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_40_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_250_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_60_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_350_2016/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_80_2016/None/USER', 25000),

_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_60_2017/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_80_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_150_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_40_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_250_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_60_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_350_2017/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_80_2017/None/USER', 25000),

_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_100_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_150_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M600_60_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_350_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau0p1mm_M800_80_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_100_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_150_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M400_40_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_250_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10000mm_M800_80_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_100_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M1000_450_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_150_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M400_40_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_250_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M600_60_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_350_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1000mm_M800_80_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_100_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M1000_450_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_150_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_250_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M600_60_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau100mm_M800_80_2018/None/USER', 23500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_100_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M1000_450_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_150_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M400_40_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M600_60_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_350_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau10mm_M800_80_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_100_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M1000_450_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_150_2018/None/USER', 24000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M400_40_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_250_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M600_60_2018/None/USER', 24500),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_350_2018/None/USER', 25000),
_adbp('miniaod', '/mfv_HtoLLPto4b_tau1mm_M800_80_2018/None/USER', 24500),

_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2016/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2016/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2016/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2016/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2016/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2016/None/USER', 5000),

_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017/None/USER', 5000),

_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2018/None/USER', 4000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2018/None/USER', 4000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2018/None/USER', 4000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2018/None/USER', 3000),

_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2016/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2016/None/USER', 5000),

_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017/None/USER', 5000),

_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2018/None/USER', 4500),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2018/None/USER', 5000),
_adbp('miniaod', '/mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2018/None/USER', 5000),

########
# ntuples
########

for x in data_samples_2017 + qcd_samples_2017 + data_samples_2018 + qcd_samples_2018:
    x.add_dataset("nr_trackingtreerv23mv3")
    x.add_dataset("nr_k0ntuplev25mv1")

for x in data_samples_2017 + qcd_samples_2017 + ttbar_samples_2017 + all_signal_samples_2017 + \
         data_samples_2018 + qcd_samples_2018 + ttbar_samples_2018 + all_signal_samples_2018:
    x.add_dataset("ntuplev27m")
    if not x.is_signal:
        x.add_dataset("ntuplev27m_ntkseeds")
        x.add_dataset("ntuplev27m_norefitdzcut")
        x.add_dataset("nr_trackmoverv27mv1")
        x.add_dataset("nr_trackmoverv27mv1_norefitdzcut")
mfv_neu_tau010000um_M0800_2017.add_dataset('ntuplev27m_norefitdzcut')

for x in all_signal_samples_2017 + all_signal_samples_2018:
    x.add_dataset("ntuplev27m_norescaling")
    if x not in (mfv_stopdbardbar_tau001000um_M0800_2018, mfv_neu_tau001000um_M1600_2018):
        x.add_dataset("ntuplev27m_wgen")

for x in all_signal_samples_2017 + all_signal_samples_2018:
    x.add_dataset("nr_trackmovermctruthv27mv1")
    x.add_dataset("nr_trackmovermctruthv27mv1_norefitdzcut")
    x.add_dataset("nr_trackmovermctruthv27mv2")

for x in mfv_splitSUSY_samples_2017 + mfv_splitSUSY_samples_2018 :
    x.add_dataset("ntuplev27m")

for x in mfv_neu_tau000100um_M0400_2018, mfv_neu_tau000100um_M0600_2018, mfv_neu_tau000100um_M0800_2018, mfv_neu_tau000100um_M1200_2018, mfv_neu_tau000100um_M1600_2018, mfv_neu_tau000100um_M3000_2018, mfv_neu_tau000300um_M0400_2018, mfv_neu_tau000300um_M0600_2018, mfv_neu_tau000300um_M0800_2018, mfv_neu_tau000300um_M1200_2018, mfv_neu_tau000300um_M1600_2018, mfv_neu_tau000300um_M3000_2018, mfv_neu_tau001000um_M0400_2018, mfv_neu_tau001000um_M0600_2018, mfv_neu_tau001000um_M0800_2018, mfv_neu_tau001000um_M1200_2018, mfv_neu_tau001000um_M1600_2018, mfv_neu_tau001000um_M3000_2018, mfv_neu_tau010000um_M0400_2018, mfv_neu_tau010000um_M0600_2018, mfv_neu_tau010000um_M0800_2018, mfv_neu_tau010000um_M1200_2018, mfv_neu_tau010000um_M1600_2018, mfv_neu_tau010000um_M3000_2018, mfv_neu_tau030000um_M0400_2018, mfv_neu_tau030000um_M0600_2018, mfv_neu_tau030000um_M0800_2018, mfv_neu_tau030000um_M1200_2018, mfv_neu_tau030000um_M1600_2018, mfv_neu_tau030000um_M3000_2018, mfv_stopdbardbar_tau000100um_M0400_2018, mfv_stopdbardbar_tau000100um_M0600_2018, mfv_stopdbardbar_tau000100um_M0800_2018, mfv_stopdbardbar_tau000100um_M1200_2018, mfv_stopdbardbar_tau000100um_M1600_2018, mfv_stopdbardbar_tau000100um_M3000_2018, mfv_stopdbardbar_tau000300um_M0400_2018, mfv_stopdbardbar_tau000300um_M0600_2018, mfv_stopdbardbar_tau000300um_M0800_2018, mfv_stopdbardbar_tau000300um_M1200_2018, mfv_stopdbardbar_tau000300um_M1600_2018, mfv_stopdbardbar_tau000300um_M3000_2018, mfv_stopdbardbar_tau001000um_M0400_2018, mfv_stopdbardbar_tau001000um_M0600_2018, mfv_stopdbardbar_tau001000um_M0800_2018, mfv_stopdbardbar_tau001000um_M1200_2018, mfv_stopdbardbar_tau001000um_M1600_2018, mfv_stopdbardbar_tau001000um_M3000_2018, mfv_stopdbardbar_tau010000um_M0400_2018, mfv_stopdbardbar_tau010000um_M0600_2018, mfv_stopdbardbar_tau010000um_M0800_2018, mfv_stopdbardbar_tau010000um_M1200_2018, mfv_stopdbardbar_tau010000um_M1600_2018, mfv_stopdbardbar_tau010000um_M3000_2018, mfv_stopdbardbar_tau030000um_M0400_2018, mfv_stopdbardbar_tau030000um_M0600_2018, mfv_stopdbardbar_tau030000um_M0800_2018, mfv_stopdbardbar_tau030000um_M1200_2018, mfv_stopdbardbar_tau030000um_M1600_2018, mfv_stopdbardbar_tau030000um_M3000_2018:
    x.add_dataset("ntuplev27lhapdfm")


singletop_tchan_top_2017.add_dataset('ntuplev28bm', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_2017-283eecf66b16e33c5d0ced53996ceea7/USER', 4336)
singletop_tchan_antitop_2017.add_dataset('ntuplev28bm', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_2017-f3c243cb29cdedee385e0375ca43ddd0/USER', 2653)
for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, qcdht0300_2017, qcdht0500_2017, ttbar_2017, ttHbb_2017, ttZ_2017, ttZext_2017, mfv_neu_tau000100um_M0400_2017, mfv_neu_tau000100um_M0600_2017, mfv_neu_tau000100um_M0800_2017, mfv_neu_tau000100um_M1200_2017, mfv_neu_tau000100um_M1600_2017, mfv_neu_tau000100um_M3000_2017, mfv_neu_tau000300um_M0400_2017, mfv_neu_tau000300um_M0600_2017, mfv_neu_tau000300um_M0800_2017, mfv_neu_tau000300um_M1200_2017, mfv_neu_tau000300um_M1600_2017, mfv_neu_tau000300um_M3000_2017, mfv_neu_tau001000um_M0400_2017, mfv_neu_tau001000um_M0600_2017, mfv_neu_tau001000um_M0800_2017, mfv_neu_tau001000um_M1200_2017, mfv_neu_tau001000um_M1600_2017, mfv_neu_tau001000um_M3000_2017, mfv_neu_tau010000um_M0400_2017, mfv_neu_tau010000um_M0600_2017, mfv_neu_tau010000um_M0800_2017, mfv_neu_tau010000um_M1200_2017, mfv_neu_tau010000um_M1600_2017, mfv_neu_tau010000um_M3000_2017, mfv_neu_tau030000um_M0400_2017, mfv_neu_tau030000um_M0600_2017, mfv_neu_tau030000um_M0800_2017, mfv_neu_tau030000um_M1200_2017, mfv_neu_tau030000um_M1600_2017, mfv_neu_tau030000um_M3000_2017, mfv_stopdbardbar_tau000100um_M0400_2017, mfv_stopdbardbar_tau000100um_M0600_2017, mfv_stopdbardbar_tau000100um_M0800_2017, mfv_stopdbardbar_tau000100um_M1200_2017, mfv_stopdbardbar_tau000100um_M1600_2017, mfv_stopdbardbar_tau000100um_M3000_2017, mfv_stopdbardbar_tau000300um_M0400_2017, mfv_stopdbardbar_tau000300um_M0600_2017, mfv_stopdbardbar_tau000300um_M0800_2017, mfv_stopdbardbar_tau000300um_M1200_2017, mfv_stopdbardbar_tau000300um_M1600_2017, mfv_stopdbardbar_tau000300um_M3000_2017, mfv_stopdbardbar_tau001000um_M0400_2017, mfv_stopdbardbar_tau001000um_M0600_2017, mfv_stopdbardbar_tau001000um_M0800_2017, mfv_stopdbardbar_tau001000um_M1200_2017, mfv_stopdbardbar_tau001000um_M1600_2017, mfv_stopdbardbar_tau001000um_M3000_2017, mfv_stopdbardbar_tau010000um_M0400_2017, mfv_stopdbardbar_tau010000um_M0600_2017, mfv_stopdbardbar_tau010000um_M0800_2017, mfv_stopdbardbar_tau010000um_M1200_2017, mfv_stopdbardbar_tau010000um_M1600_2017, mfv_stopdbardbar_tau010000um_M3000_2017, mfv_stopdbardbar_tau030000um_M0400_2017, mfv_stopdbardbar_tau030000um_M0600_2017, mfv_stopdbardbar_tau030000um_M0800_2017, mfv_stopdbardbar_tau030000um_M1200_2017, mfv_stopdbardbar_tau030000um_M1600_2017, mfv_stopdbardbar_tau030000um_M3000_2017:
    x.add_dataset("ntuplev28bm")

singletop_tchan_top_2017.add_dataset('ntuplev28bm_ntkseeds', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_NTkSeeds_2017-4fd43c30c720063db8c53a24e852c239/USER', 6619)
singletop_tchan_antitop_2017.add_dataset('ntuplev28bm_ntkseeds', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_NTkSeeds_2017-c23d1a276623eee9668ca7711bbfadef/USER', 2731)
for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, qcdht0300_2017, qcdht0500_2017, ttbar_2017, ttHbb_2017, ttZ_2017, ttZext_2017:
    x.add_dataset("ntuplev28bm_ntkseeds")


for x in mfv_HtoLLPto4j_tau0p1mm_M1000_100_2017, mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017, mfv_HtoLLPto4j_tau0p1mm_M400_150_2017, mfv_HtoLLPto4j_tau0p1mm_M400_40_2017, mfv_HtoLLPto4j_tau0p1mm_M600_250_2017, mfv_HtoLLPto4j_tau0p1mm_M600_60_2017, mfv_HtoLLPto4j_tau0p1mm_M800_350_2017, mfv_HtoLLPto4j_tau0p1mm_M800_80_2017, mfv_HtoLLPto4j_tau10000mm_M1000_100_2017, mfv_HtoLLPto4j_tau10000mm_M1000_450_2017, mfv_HtoLLPto4j_tau10000mm_M400_150_2017, mfv_HtoLLPto4j_tau10000mm_M400_40_2017, mfv_HtoLLPto4j_tau10000mm_M600_250_2017, mfv_HtoLLPto4j_tau10000mm_M600_60_2017, mfv_HtoLLPto4j_tau10000mm_M800_350_2017, mfv_HtoLLPto4j_tau10000mm_M800_80_2017, mfv_HtoLLPto4j_tau1000mm_M1000_100_2017, mfv_HtoLLPto4j_tau1000mm_M1000_450_2017, mfv_HtoLLPto4j_tau1000mm_M400_150_2017, mfv_HtoLLPto4j_tau1000mm_M400_40_2017, mfv_HtoLLPto4j_tau1000mm_M600_250_2017, mfv_HtoLLPto4j_tau1000mm_M600_60_2017, mfv_HtoLLPto4j_tau1000mm_M800_350_2017, mfv_HtoLLPto4j_tau1000mm_M800_80_2017, mfv_HtoLLPto4j_tau100mm_M1000_100_2017, mfv_HtoLLPto4j_tau100mm_M1000_450_2017, mfv_HtoLLPto4j_tau100mm_M400_150_2017, mfv_HtoLLPto4j_tau100mm_M400_40_2017, mfv_HtoLLPto4j_tau100mm_M600_250_2017, mfv_HtoLLPto4j_tau100mm_M600_60_2017, mfv_HtoLLPto4j_tau100mm_M800_350_2017, mfv_HtoLLPto4j_tau100mm_M800_80_2017, mfv_HtoLLPto4j_tau10mm_M1000_100_2017, mfv_HtoLLPto4j_tau10mm_M1000_450_2017, mfv_HtoLLPto4j_tau10mm_M400_150_2017, mfv_HtoLLPto4j_tau10mm_M400_40_2017, mfv_HtoLLPto4j_tau10mm_M600_250_2017, mfv_HtoLLPto4j_tau10mm_M600_60_2017, mfv_HtoLLPto4j_tau10mm_M800_350_2017, mfv_HtoLLPto4j_tau10mm_M800_80_2017, mfv_HtoLLPto4j_tau1mm_M1000_100_2017, mfv_HtoLLPto4j_tau1mm_M1000_450_2017, mfv_HtoLLPto4j_tau1mm_M400_150_2017, mfv_HtoLLPto4j_tau1mm_M400_40_2017, mfv_HtoLLPto4j_tau1mm_M600_250_2017, mfv_HtoLLPto4j_tau1mm_M600_60_2017, mfv_HtoLLPto4j_tau1mm_M800_350_2017, mfv_HtoLLPto4j_tau1mm_M800_80_2017, mfv_HtoLLPto4j_tau0p1mm_M1000_100_2018, mfv_HtoLLPto4j_tau0p1mm_M1000_450_2018, mfv_HtoLLPto4j_tau0p1mm_M400_150_2018, mfv_HtoLLPto4j_tau0p1mm_M400_40_2018, mfv_HtoLLPto4j_tau0p1mm_M600_250_2018, mfv_HtoLLPto4j_tau0p1mm_M600_60_2018, mfv_HtoLLPto4j_tau0p1mm_M800_350_2018, mfv_HtoLLPto4j_tau0p1mm_M800_80_2018, mfv_HtoLLPto4j_tau10000mm_M1000_100_2018, mfv_HtoLLPto4j_tau10000mm_M1000_450_2018, mfv_HtoLLPto4j_tau10000mm_M400_150_2018, mfv_HtoLLPto4j_tau10000mm_M400_40_2018, mfv_HtoLLPto4j_tau10000mm_M600_250_2018, mfv_HtoLLPto4j_tau10000mm_M600_60_2018, mfv_HtoLLPto4j_tau10000mm_M800_350_2018, mfv_HtoLLPto4j_tau10000mm_M800_80_2018, mfv_HtoLLPto4j_tau1000mm_M1000_100_2018, mfv_HtoLLPto4j_tau1000mm_M1000_450_2018, mfv_HtoLLPto4j_tau1000mm_M400_150_2018, mfv_HtoLLPto4j_tau1000mm_M400_40_2018, mfv_HtoLLPto4j_tau1000mm_M600_250_2018, mfv_HtoLLPto4j_tau1000mm_M600_60_2018, mfv_HtoLLPto4j_tau1000mm_M800_350_2018, mfv_HtoLLPto4j_tau1000mm_M800_80_2018, mfv_HtoLLPto4j_tau100mm_M1000_100_2018, mfv_HtoLLPto4j_tau100mm_M1000_450_2018, mfv_HtoLLPto4j_tau100mm_M400_150_2018, mfv_HtoLLPto4j_tau100mm_M400_40_2018, mfv_HtoLLPto4j_tau100mm_M600_250_2018, mfv_HtoLLPto4j_tau100mm_M600_60_2018, mfv_HtoLLPto4j_tau100mm_M800_350_2018, mfv_HtoLLPto4j_tau100mm_M800_80_2018, mfv_HtoLLPto4j_tau10mm_M1000_100_2018, mfv_HtoLLPto4j_tau10mm_M1000_450_2018, mfv_HtoLLPto4j_tau10mm_M400_150_2018, mfv_HtoLLPto4j_tau10mm_M400_40_2018, mfv_HtoLLPto4j_tau10mm_M600_250_2018, mfv_HtoLLPto4j_tau10mm_M600_60_2018, mfv_HtoLLPto4j_tau10mm_M800_350_2018, mfv_HtoLLPto4j_tau10mm_M800_80_2018, mfv_HtoLLPto4j_tau1mm_M1000_100_2018, mfv_HtoLLPto4j_tau1mm_M1000_450_2018, mfv_HtoLLPto4j_tau1mm_M400_150_2018, mfv_HtoLLPto4j_tau1mm_M400_40_2018, mfv_HtoLLPto4j_tau1mm_M600_250_2018, mfv_HtoLLPto4j_tau1mm_M600_60_2018, mfv_HtoLLPto4j_tau1mm_M800_350_2018, mfv_HtoLLPto4j_tau1mm_M800_80_2018, mfv_HtoLLPto4b_tau0p1mm_M1000_100_2017, mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017, mfv_HtoLLPto4b_tau0p1mm_M400_150_2017, mfv_HtoLLPto4b_tau0p1mm_M400_40_2017, mfv_HtoLLPto4b_tau0p1mm_M600_250_2017, mfv_HtoLLPto4b_tau0p1mm_M600_60_2017, mfv_HtoLLPto4b_tau0p1mm_M800_350_2017, mfv_HtoLLPto4b_tau0p1mm_M800_80_2017, mfv_HtoLLPto4b_tau10000mm_M1000_100_2017, mfv_HtoLLPto4b_tau10000mm_M1000_450_2017, mfv_HtoLLPto4b_tau10000mm_M400_150_2017, mfv_HtoLLPto4b_tau10000mm_M400_40_2017, mfv_HtoLLPto4b_tau10000mm_M600_250_2017, mfv_HtoLLPto4b_tau10000mm_M600_60_2017, mfv_HtoLLPto4b_tau10000mm_M800_350_2017, mfv_HtoLLPto4b_tau10000mm_M800_80_2017, mfv_HtoLLPto4b_tau1000mm_M1000_100_2017, mfv_HtoLLPto4b_tau1000mm_M1000_450_2017, mfv_HtoLLPto4b_tau1000mm_M400_150_2017, mfv_HtoLLPto4b_tau1000mm_M400_40_2017, mfv_HtoLLPto4b_tau1000mm_M600_250_2017, mfv_HtoLLPto4b_tau1000mm_M600_60_2017, mfv_HtoLLPto4b_tau1000mm_M800_350_2017, mfv_HtoLLPto4b_tau1000mm_M800_80_2017, mfv_HtoLLPto4b_tau100mm_M1000_100_2017, mfv_HtoLLPto4b_tau100mm_M1000_450_2017, mfv_HtoLLPto4b_tau100mm_M400_150_2017, mfv_HtoLLPto4b_tau100mm_M400_40_2017, mfv_HtoLLPto4b_tau100mm_M600_250_2017, mfv_HtoLLPto4b_tau100mm_M600_60_2017, mfv_HtoLLPto4b_tau100mm_M800_350_2017, mfv_HtoLLPto4b_tau100mm_M800_80_2017, mfv_HtoLLPto4b_tau10mm_M1000_100_2017, mfv_HtoLLPto4b_tau10mm_M1000_450_2017, mfv_HtoLLPto4b_tau10mm_M400_150_2017, mfv_HtoLLPto4b_tau10mm_M400_40_2017, mfv_HtoLLPto4b_tau10mm_M600_250_2017, mfv_HtoLLPto4b_tau10mm_M600_60_2017, mfv_HtoLLPto4b_tau10mm_M800_350_2017, mfv_HtoLLPto4b_tau10mm_M800_80_2017, mfv_HtoLLPto4b_tau1mm_M1000_100_2017, mfv_HtoLLPto4b_tau1mm_M1000_450_2017, mfv_HtoLLPto4b_tau1mm_M400_150_2017, mfv_HtoLLPto4b_tau1mm_M400_40_2017, mfv_HtoLLPto4b_tau1mm_M600_250_2017, mfv_HtoLLPto4b_tau1mm_M600_60_2017, mfv_HtoLLPto4b_tau1mm_M800_350_2017, mfv_HtoLLPto4b_tau1mm_M800_80_2017, mfv_HtoLLPto4b_tau0p1mm_M1000_100_2018, mfv_HtoLLPto4b_tau0p1mm_M1000_450_2018, mfv_HtoLLPto4b_tau0p1mm_M400_150_2018, mfv_HtoLLPto4b_tau0p1mm_M400_40_2018, mfv_HtoLLPto4b_tau0p1mm_M600_250_2018, mfv_HtoLLPto4b_tau0p1mm_M600_60_2018, mfv_HtoLLPto4b_tau0p1mm_M800_350_2018, mfv_HtoLLPto4b_tau0p1mm_M800_80_2018, mfv_HtoLLPto4b_tau10000mm_M1000_100_2018, mfv_HtoLLPto4b_tau10000mm_M1000_450_2018, mfv_HtoLLPto4b_tau10000mm_M400_150_2018, mfv_HtoLLPto4b_tau10000mm_M400_40_2018, mfv_HtoLLPto4b_tau10000mm_M600_250_2018, mfv_HtoLLPto4b_tau10000mm_M600_60_2018, mfv_HtoLLPto4b_tau10000mm_M800_350_2018, mfv_HtoLLPto4b_tau10000mm_M800_80_2018, mfv_HtoLLPto4b_tau1000mm_M1000_100_2018, mfv_HtoLLPto4b_tau1000mm_M1000_450_2018, mfv_HtoLLPto4b_tau1000mm_M400_150_2018, mfv_HtoLLPto4b_tau1000mm_M400_40_2018, mfv_HtoLLPto4b_tau1000mm_M600_250_2018, mfv_HtoLLPto4b_tau1000mm_M600_60_2018, mfv_HtoLLPto4b_tau1000mm_M800_350_2018, mfv_HtoLLPto4b_tau1000mm_M800_80_2018, mfv_HtoLLPto4b_tau100mm_M1000_100_2018, mfv_HtoLLPto4b_tau100mm_M1000_450_2018, mfv_HtoLLPto4b_tau100mm_M400_150_2018, mfv_HtoLLPto4b_tau100mm_M400_40_2018, mfv_HtoLLPto4b_tau100mm_M600_250_2018, mfv_HtoLLPto4b_tau100mm_M600_60_2018, mfv_HtoLLPto4b_tau100mm_M800_350_2018, mfv_HtoLLPto4b_tau100mm_M800_80_2018, mfv_HtoLLPto4b_tau10mm_M1000_100_2018, mfv_HtoLLPto4b_tau10mm_M1000_450_2018, mfv_HtoLLPto4b_tau10mm_M400_150_2018, mfv_HtoLLPto4b_tau10mm_M400_40_2018, mfv_HtoLLPto4b_tau10mm_M600_250_2018, mfv_HtoLLPto4b_tau10mm_M600_60_2018, mfv_HtoLLPto4b_tau10mm_M800_350_2018, mfv_HtoLLPto4b_tau10mm_M800_80_2018, mfv_HtoLLPto4b_tau1mm_M1000_100_2018, mfv_HtoLLPto4b_tau1mm_M1000_450_2018, mfv_HtoLLPto4b_tau1mm_M400_150_2018, mfv_HtoLLPto4b_tau1mm_M400_40_2018, mfv_HtoLLPto4b_tau1mm_M600_250_2018, mfv_HtoLLPto4b_tau1mm_M600_60_2018, mfv_HtoLLPto4b_tau1mm_M800_350_2018, mfv_HtoLLPto4b_tau1mm_M800_80_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2018:
    x.add_dataset("ntuplev27darksectorreviewm")

for x in mfv_HtoLLPto4j_tau0p1mm_M1000_100_2017, mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017, mfv_HtoLLPto4j_tau0p1mm_M400_150_2017, mfv_HtoLLPto4j_tau0p1mm_M400_40_2017, mfv_HtoLLPto4j_tau0p1mm_M600_250_2017, mfv_HtoLLPto4j_tau0p1mm_M600_60_2017, mfv_HtoLLPto4j_tau0p1mm_M800_350_2017, mfv_HtoLLPto4j_tau0p1mm_M800_80_2017, mfv_HtoLLPto4j_tau10000mm_M1000_100_2017, mfv_HtoLLPto4j_tau10000mm_M1000_450_2017, mfv_HtoLLPto4j_tau10000mm_M400_150_2017, mfv_HtoLLPto4j_tau10000mm_M400_40_2017, mfv_HtoLLPto4j_tau10000mm_M600_250_2017, mfv_HtoLLPto4j_tau10000mm_M600_60_2017, mfv_HtoLLPto4j_tau10000mm_M800_350_2017, mfv_HtoLLPto4j_tau10000mm_M800_80_2017, mfv_HtoLLPto4j_tau1000mm_M1000_100_2017, mfv_HtoLLPto4j_tau1000mm_M1000_450_2017, mfv_HtoLLPto4j_tau1000mm_M400_150_2017, mfv_HtoLLPto4j_tau1000mm_M400_40_2017, mfv_HtoLLPto4j_tau1000mm_M600_250_2017, mfv_HtoLLPto4j_tau1000mm_M600_60_2017, mfv_HtoLLPto4j_tau1000mm_M800_350_2017, mfv_HtoLLPto4j_tau1000mm_M800_80_2017, mfv_HtoLLPto4j_tau100mm_M1000_100_2017, mfv_HtoLLPto4j_tau100mm_M1000_450_2017, mfv_HtoLLPto4j_tau100mm_M400_150_2017, mfv_HtoLLPto4j_tau100mm_M400_40_2017, mfv_HtoLLPto4j_tau100mm_M600_250_2017, mfv_HtoLLPto4j_tau100mm_M600_60_2017, mfv_HtoLLPto4j_tau100mm_M800_350_2017, mfv_HtoLLPto4j_tau100mm_M800_80_2017, mfv_HtoLLPto4j_tau10mm_M1000_100_2017, mfv_HtoLLPto4j_tau10mm_M1000_450_2017, mfv_HtoLLPto4j_tau10mm_M400_150_2017, mfv_HtoLLPto4j_tau10mm_M400_40_2017, mfv_HtoLLPto4j_tau10mm_M600_250_2017, mfv_HtoLLPto4j_tau10mm_M600_60_2017, mfv_HtoLLPto4j_tau10mm_M800_350_2017, mfv_HtoLLPto4j_tau10mm_M800_80_2017, mfv_HtoLLPto4j_tau1mm_M1000_100_2017, mfv_HtoLLPto4j_tau1mm_M1000_450_2017, mfv_HtoLLPto4j_tau1mm_M400_150_2017, mfv_HtoLLPto4j_tau1mm_M400_40_2017, mfv_HtoLLPto4j_tau1mm_M600_250_2017, mfv_HtoLLPto4j_tau1mm_M600_60_2017, mfv_HtoLLPto4j_tau1mm_M800_350_2017, mfv_HtoLLPto4j_tau1mm_M800_80_2017, mfv_HtoLLPto4j_tau0p1mm_M1000_100_2018, mfv_HtoLLPto4j_tau0p1mm_M1000_450_2018, mfv_HtoLLPto4j_tau0p1mm_M400_150_2018, mfv_HtoLLPto4j_tau0p1mm_M400_40_2018, mfv_HtoLLPto4j_tau0p1mm_M600_250_2018, mfv_HtoLLPto4j_tau0p1mm_M600_60_2018, mfv_HtoLLPto4j_tau0p1mm_M800_350_2018, mfv_HtoLLPto4j_tau0p1mm_M800_80_2018, mfv_HtoLLPto4j_tau10000mm_M1000_100_2018, mfv_HtoLLPto4j_tau10000mm_M1000_450_2018, mfv_HtoLLPto4j_tau10000mm_M400_150_2018, mfv_HtoLLPto4j_tau10000mm_M400_40_2018, mfv_HtoLLPto4j_tau10000mm_M600_250_2018, mfv_HtoLLPto4j_tau10000mm_M600_60_2018, mfv_HtoLLPto4j_tau10000mm_M800_350_2018, mfv_HtoLLPto4j_tau10000mm_M800_80_2018, mfv_HtoLLPto4j_tau1000mm_M1000_100_2018, mfv_HtoLLPto4j_tau1000mm_M1000_450_2018, mfv_HtoLLPto4j_tau1000mm_M400_150_2018, mfv_HtoLLPto4j_tau1000mm_M400_40_2018, mfv_HtoLLPto4j_tau1000mm_M600_250_2018, mfv_HtoLLPto4j_tau1000mm_M600_60_2018, mfv_HtoLLPto4j_tau1000mm_M800_350_2018, mfv_HtoLLPto4j_tau1000mm_M800_80_2018, mfv_HtoLLPto4j_tau100mm_M1000_100_2018, mfv_HtoLLPto4j_tau100mm_M1000_450_2018, mfv_HtoLLPto4j_tau100mm_M400_150_2018, mfv_HtoLLPto4j_tau100mm_M400_40_2018, mfv_HtoLLPto4j_tau100mm_M600_250_2018, mfv_HtoLLPto4j_tau100mm_M600_60_2018, mfv_HtoLLPto4j_tau100mm_M800_350_2018, mfv_HtoLLPto4j_tau100mm_M800_80_2018, mfv_HtoLLPto4j_tau10mm_M1000_100_2018, mfv_HtoLLPto4j_tau10mm_M1000_450_2018, mfv_HtoLLPto4j_tau10mm_M400_150_2018, mfv_HtoLLPto4j_tau10mm_M400_40_2018, mfv_HtoLLPto4j_tau10mm_M600_250_2018, mfv_HtoLLPto4j_tau10mm_M600_60_2018, mfv_HtoLLPto4j_tau10mm_M800_350_2018, mfv_HtoLLPto4j_tau10mm_M800_80_2018, mfv_HtoLLPto4j_tau1mm_M1000_100_2018, mfv_HtoLLPto4j_tau1mm_M1000_450_2018, mfv_HtoLLPto4j_tau1mm_M400_150_2018, mfv_HtoLLPto4j_tau1mm_M400_40_2018, mfv_HtoLLPto4j_tau1mm_M600_250_2018, mfv_HtoLLPto4j_tau1mm_M600_60_2018, mfv_HtoLLPto4j_tau1mm_M800_350_2018, mfv_HtoLLPto4j_tau1mm_M800_80_2018, mfv_HtoLLPto4b_tau0p1mm_M1000_100_2017, mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017, mfv_HtoLLPto4b_tau0p1mm_M400_150_2017, mfv_HtoLLPto4b_tau0p1mm_M400_40_2017, mfv_HtoLLPto4b_tau0p1mm_M600_250_2017, mfv_HtoLLPto4b_tau0p1mm_M600_60_2017, mfv_HtoLLPto4b_tau0p1mm_M800_350_2017, mfv_HtoLLPto4b_tau0p1mm_M800_80_2017, mfv_HtoLLPto4b_tau10000mm_M1000_100_2017, mfv_HtoLLPto4b_tau10000mm_M1000_450_2017, mfv_HtoLLPto4b_tau10000mm_M400_150_2017, mfv_HtoLLPto4b_tau10000mm_M400_40_2017, mfv_HtoLLPto4b_tau10000mm_M600_250_2017, mfv_HtoLLPto4b_tau10000mm_M600_60_2017, mfv_HtoLLPto4b_tau10000mm_M800_350_2017, mfv_HtoLLPto4b_tau10000mm_M800_80_2017, mfv_HtoLLPto4b_tau1000mm_M1000_100_2017, mfv_HtoLLPto4b_tau1000mm_M1000_450_2017, mfv_HtoLLPto4b_tau1000mm_M400_150_2017, mfv_HtoLLPto4b_tau1000mm_M400_40_2017, mfv_HtoLLPto4b_tau1000mm_M600_250_2017, mfv_HtoLLPto4b_tau1000mm_M600_60_2017, mfv_HtoLLPto4b_tau1000mm_M800_350_2017, mfv_HtoLLPto4b_tau1000mm_M800_80_2017, mfv_HtoLLPto4b_tau100mm_M1000_100_2017, mfv_HtoLLPto4b_tau100mm_M1000_450_2017, mfv_HtoLLPto4b_tau100mm_M400_150_2017, mfv_HtoLLPto4b_tau100mm_M400_40_2017, mfv_HtoLLPto4b_tau100mm_M600_250_2017, mfv_HtoLLPto4b_tau100mm_M600_60_2017, mfv_HtoLLPto4b_tau100mm_M800_350_2017, mfv_HtoLLPto4b_tau100mm_M800_80_2017, mfv_HtoLLPto4b_tau10mm_M1000_100_2017, mfv_HtoLLPto4b_tau10mm_M1000_450_2017, mfv_HtoLLPto4b_tau10mm_M400_150_2017, mfv_HtoLLPto4b_tau10mm_M400_40_2017, mfv_HtoLLPto4b_tau10mm_M600_250_2017, mfv_HtoLLPto4b_tau10mm_M600_60_2017, mfv_HtoLLPto4b_tau10mm_M800_350_2017, mfv_HtoLLPto4b_tau10mm_M800_80_2017, mfv_HtoLLPto4b_tau1mm_M1000_100_2017, mfv_HtoLLPto4b_tau1mm_M1000_450_2017, mfv_HtoLLPto4b_tau1mm_M400_150_2017, mfv_HtoLLPto4b_tau1mm_M400_40_2017, mfv_HtoLLPto4b_tau1mm_M600_250_2017, mfv_HtoLLPto4b_tau1mm_M600_60_2017, mfv_HtoLLPto4b_tau1mm_M800_350_2017, mfv_HtoLLPto4b_tau1mm_M800_80_2017, mfv_HtoLLPto4b_tau0p1mm_M1000_100_2018, mfv_HtoLLPto4b_tau0p1mm_M1000_450_2018, mfv_HtoLLPto4b_tau0p1mm_M400_150_2018, mfv_HtoLLPto4b_tau0p1mm_M400_40_2018, mfv_HtoLLPto4b_tau0p1mm_M600_250_2018, mfv_HtoLLPto4b_tau0p1mm_M600_60_2018, mfv_HtoLLPto4b_tau0p1mm_M800_350_2018, mfv_HtoLLPto4b_tau0p1mm_M800_80_2018, mfv_HtoLLPto4b_tau10000mm_M1000_100_2018, mfv_HtoLLPto4b_tau10000mm_M1000_450_2018, mfv_HtoLLPto4b_tau10000mm_M400_150_2018, mfv_HtoLLPto4b_tau10000mm_M400_40_2018, mfv_HtoLLPto4b_tau10000mm_M600_250_2018, mfv_HtoLLPto4b_tau10000mm_M600_60_2018, mfv_HtoLLPto4b_tau10000mm_M800_350_2018, mfv_HtoLLPto4b_tau10000mm_M800_80_2018, mfv_HtoLLPto4b_tau1000mm_M1000_100_2018, mfv_HtoLLPto4b_tau1000mm_M1000_450_2018, mfv_HtoLLPto4b_tau1000mm_M400_150_2018, mfv_HtoLLPto4b_tau1000mm_M400_40_2018, mfv_HtoLLPto4b_tau1000mm_M600_250_2018, mfv_HtoLLPto4b_tau1000mm_M600_60_2018, mfv_HtoLLPto4b_tau1000mm_M800_350_2018, mfv_HtoLLPto4b_tau1000mm_M800_80_2018, mfv_HtoLLPto4b_tau100mm_M1000_100_2018, mfv_HtoLLPto4b_tau100mm_M1000_450_2018, mfv_HtoLLPto4b_tau100mm_M400_150_2018, mfv_HtoLLPto4b_tau100mm_M400_40_2018, mfv_HtoLLPto4b_tau100mm_M600_250_2018, mfv_HtoLLPto4b_tau100mm_M600_60_2018, mfv_HtoLLPto4b_tau100mm_M800_350_2018, mfv_HtoLLPto4b_tau100mm_M800_80_2018, mfv_HtoLLPto4b_tau10mm_M1000_100_2018, mfv_HtoLLPto4b_tau10mm_M1000_450_2018, mfv_HtoLLPto4b_tau10mm_M400_150_2018, mfv_HtoLLPto4b_tau10mm_M400_40_2018, mfv_HtoLLPto4b_tau10mm_M600_250_2018, mfv_HtoLLPto4b_tau10mm_M600_60_2018, mfv_HtoLLPto4b_tau10mm_M800_350_2018, mfv_HtoLLPto4b_tau10mm_M800_80_2018, mfv_HtoLLPto4b_tau1mm_M1000_100_2018, mfv_HtoLLPto4b_tau1mm_M1000_450_2018, mfv_HtoLLPto4b_tau1mm_M400_150_2018, mfv_HtoLLPto4b_tau1mm_M400_40_2018, mfv_HtoLLPto4b_tau1mm_M600_250_2018, mfv_HtoLLPto4b_tau1mm_M600_60_2018, mfv_HtoLLPto4b_tau1mm_M800_350_2018, mfv_HtoLLPto4b_tau1mm_M800_80_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017, mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017, mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017, mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017, mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017, mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017, mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017, mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017, mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017, mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017, mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017, mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017, mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017, mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017, mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017, mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2018, mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2018, mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2018, mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2018, mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2018, mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2018, mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2018, mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2018, mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2018, mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2018, mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2018, mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2018, mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2018, mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2018, mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2018, mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2018, mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017, mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017, mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017, mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017, mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017, mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017, mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017, mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017, mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017, mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017, mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017, mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017, mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017, mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017, mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017, mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2018, mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2018, mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2018, mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2018, mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2018, mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2018, mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2018, mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2018, mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2018, mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2018, mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2018, mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2018, mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2018, mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2018, mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2018, mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2018, mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2018:
    x.add_dataset("ntuplev27darksectorreview_withgeninfom")

########
# automatic condor declarations for ntuples
########

for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in 'ntuple', 'nr_':
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########

condorable = {
    "T3_US_FNALLPC": {
        "miniaod": mfv_splitSUSY_samples_2016 + mfv_splitSUSY_samples_2017 + mfv_splitSUSY_samples_2018 + mfv_HtoLLPto4j_samples_2016 + mfv_HtoLLPto4j_samples_2017 + mfv_HtoLLPto4j_samples_2018 + mfv_HtoLLPto4b_samples_2016 + mfv_HtoLLPto4b_samples_2017 + mfv_HtoLLPto4b_samples_2018 + mfv_ZprimetoLLPto4j_samples_2016 + mfv_ZprimetoLLPto4j_samples_2017 + mfv_ZprimetoLLPto4j_samples_2018 + mfv_ZprimetoLLPto4b_samples_2016 + mfv_ZprimetoLLPto4b_samples_2017 + mfv_ZprimetoLLPto4b_samples_2018 + ttbar_samples_2017 + [qcdht1000_2017, qcdht1500_2018, qcdht2000_2018, ttbarht0600_2018, ttbarht1200_2018, ttbarht2500_2018,
                                         mfv_neu_tau000100um_M0400_2017, mfv_neu_tau000100um_M0800_2017, mfv_neu_tau000100um_M1200_2017, mfv_neu_tau000100um_M1600_2017, mfv_neu_tau000100um_M3000_2017, mfv_neu_tau000300um_M0600_2017, mfv_neu_tau000300um_M1200_2017, mfv_neu_tau000300um_M1600_2017, mfv_neu_tau001000um_M0400_2017, mfv_neu_tau001000um_M0600_2017, mfv_neu_tau001000um_M0800_2017, mfv_neu_tau001000um_M1200_2017, mfv_neu_tau001000um_M1600_2017, mfv_neu_tau001000um_M3000_2017, mfv_neu_tau010000um_M0600_2017, mfv_neu_tau010000um_M1200_2017, mfv_neu_tau010000um_M3000_2017, mfv_neu_tau030000um_M0400_2017, mfv_neu_tau030000um_M0600_2017, mfv_neu_tau030000um_M1200_2017, mfv_neu_tau030000um_M1600_2017, mfv_stopdbardbar_tau000100um_M0400_2017, mfv_stopdbardbar_tau000100um_M0800_2017, mfv_stopdbardbar_tau000100um_M1200_2017, mfv_stopdbardbar_tau000100um_M3000_2017, mfv_stopdbardbar_tau000300um_M0400_2017, mfv_stopdbardbar_tau000300um_M0600_2017, mfv_stopdbardbar_tau000300um_M0800_2017, mfv_stopdbardbar_tau000300um_M1600_2017, mfv_stopdbardbar_tau000300um_M3000_2017, mfv_stopdbardbar_tau001000um_M0600_2017, mfv_stopdbardbar_tau001000um_M0800_2017, mfv_stopdbardbar_tau001000um_M1600_2017, mfv_stopdbardbar_tau010000um_M0400_2017, mfv_stopdbardbar_tau010000um_M0600_2017, mfv_stopdbardbar_tau010000um_M1200_2017, mfv_stopdbardbar_tau010000um_M1600_2017, mfv_stopdbardbar_tau030000um_M0400_2017, mfv_stopdbardbar_tau030000um_M0600_2017, mfv_stopdbardbar_tau030000um_M0800_2017, mfv_stopdbardbar_tau030000um_M3000_2017,
                                         mfv_neu_tau000100um_M0400_2018, mfv_neu_tau000100um_M0600_2018, mfv_neu_tau000100um_M0800_2018, mfv_neu_tau000100um_M1200_2018, mfv_neu_tau000100um_M1600_2018, mfv_neu_tau000100um_M3000_2018, mfv_neu_tau000300um_M0400_2018, mfv_neu_tau000300um_M0600_2018, mfv_neu_tau000300um_M0800_2018, mfv_neu_tau000300um_M1200_2018, mfv_neu_tau000300um_M1600_2018, mfv_neu_tau000300um_M3000_2018, mfv_neu_tau001000um_M0400_2018, mfv_neu_tau001000um_M0600_2018, mfv_neu_tau001000um_M1200_2018, mfv_neu_tau001000um_M1600_2018, mfv_neu_tau001000um_M3000_2018, mfv_neu_tau010000um_M0400_2018, mfv_neu_tau010000um_M0600_2018, mfv_neu_tau010000um_M0800_2018, mfv_neu_tau010000um_M1200_2018, mfv_neu_tau010000um_M1600_2018, mfv_neu_tau010000um_M3000_2018, mfv_neu_tau030000um_M0400_2018, mfv_neu_tau030000um_M0600_2018, mfv_neu_tau030000um_M0800_2018, mfv_neu_tau030000um_M1200_2018, mfv_neu_tau030000um_M1600_2018, mfv_neu_tau030000um_M3000_2018, mfv_stopdbardbar_tau000100um_M0400_2018, mfv_stopdbardbar_tau000100um_M0600_2018, mfv_stopdbardbar_tau000100um_M0800_2018, mfv_stopdbardbar_tau000100um_M1200_2018, mfv_stopdbardbar_tau000100um_M3000_2018, mfv_stopdbardbar_tau000300um_M0600_2018, mfv_stopdbardbar_tau000300um_M0800_2018, mfv_stopdbardbar_tau000300um_M1200_2018, mfv_stopdbardbar_tau000300um_M3000_2018, mfv_stopdbardbar_tau001000um_M0400_2018, mfv_stopdbardbar_tau001000um_M0600_2018, mfv_stopdbardbar_tau001000um_M0800_2018, mfv_stopdbardbar_tau001000um_M1200_2018, mfv_stopdbardbar_tau001000um_M1600_2018, mfv_stopdbardbar_tau001000um_M3000_2018, mfv_stopdbardbar_tau010000um_M0400_2018, mfv_stopdbardbar_tau010000um_M0600_2018, mfv_stopdbardbar_tau010000um_M0800_2018, mfv_stopdbardbar_tau010000um_M1600_2018, mfv_stopdbardbar_tau030000um_M0400_2018, mfv_stopdbardbar_tau030000um_M0600_2018, mfv_stopdbardbar_tau030000um_M0800_2018, mfv_stopdbardbar_tau030000um_M1200_2018, mfv_stopdbardbar_tau030000um_M3000_2018,
                                         ],
        },
    "T1_US_FNAL_Disk": {
        "miniaod": [qcdht1500_2017, qcdht2000_2017, dyjetstollM10_2017, qcdmupt15_2017, qcdht0300_2018, qcdht0700_2018, ttbarht0800_2018,
                    JetHT2017B, JetHT2017D, JetHT2017F, JetHT2018A, JetHT2018B, JetHT2018D,
                    mfv_neu_tau000100um_M0600_2017, mfv_neu_tau000300um_M0400_2017, mfv_neu_tau000300um_M0800_2017, mfv_neu_tau000300um_M3000_2017, mfv_neu_tau010000um_M0400_2017, mfv_neu_tau010000um_M0800_2017, mfv_neu_tau010000um_M1600_2017, mfv_neu_tau030000um_M0800_2017, mfv_neu_tau030000um_M3000_2017, mfv_stopdbardbar_tau000100um_M0600_2017, mfv_stopdbardbar_tau000100um_M1600_2017, mfv_stopdbardbar_tau000300um_M1200_2017, mfv_stopdbardbar_tau001000um_M0400_2017, mfv_stopdbardbar_tau001000um_M1200_2017, mfv_stopdbardbar_tau001000um_M3000_2017, mfv_stopdbardbar_tau010000um_M0800_2017, mfv_stopdbardbar_tau010000um_M3000_2017, mfv_stopdbardbar_tau030000um_M1200_2017, mfv_stopdbardbar_tau030000um_M1600_2017,
                    mfv_neu_tau001000um_M0800_2018, mfv_stopdbardbar_tau000100um_M1600_2018, mfv_stopdbardbar_tau000300um_M0400_2018, mfv_stopdbardbar_tau000300um_M1600_2018, mfv_stopdbardbar_tau010000um_M1200_2018, mfv_stopdbardbar_tau010000um_M3000_2018, mfv_stopdbardbar_tau030000um_M1600_2018, SingleMuon2017F],
        },
    "T2_DE_DESY": {
        "miniaod": [JetHT2017C, JetHT2017E, JetHT2018C, SingleMuon2017D],
        },
    "T2_US_MIT": {
        "miniaod": [qcdht0500_2018, ttHbb_2017],
        },
    "T2_US_Florida": {
        "miniaod": [ttbar_2018, ttZext_2017, qcdht0700_2017, qcdht0500_2017],
        },
    "T2_US_Nebraska": {
        "miniaod": [SingleMuon2017C, ttbar_2017, qcdht0300_2017],
        },
    "T2_US_Purdue": {
        "miniaod": [],
        },
    "T2_US_Wisconsin" : {
        "miniaod": [ttZ_2017],
        },
    }

_seen = set()
for site, d in condorable.iteritems():
    if not xrootd_sites.has_key(site):
        raise ValueError('need entry in xrootd_sites for %s' % site)
    for ds, samples in d.iteritems():
        for s in samples:
            if s in _seen:
                raise ValueError('%s duplicated in condorable dict' % s.name)
            _seen.add(s)
            s.datasets[ds].condor = True
            s.datasets[ds].xrootd_url = xrootd_sites[site]

# can only run signal ntuples via condor where we can split by nevents, so require they're all reachable
for s in mfv_signal_samples_2017 + mfv_signal_samples_2018 + mfv_stopdbardbar_samples_2017 + mfv_stopdbardbar_samples_2018:
    if s not in _seen:
        raise ValueError('%s not in condorable dict' % s.name)

########
# other info
########

for ds in 'main', 'miniaod':
    # these in status=PRODUCTION
    #for s in ():
    #    s.datasets[ds].ignore_invalid = True

    # 'PU2017' in dataset can be a lie https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3128.html
    for s in qcdht0700_2017, dyjetstollM10_2017, dyjetstollM50_2017, dyjetstollM50ext_2017:
        s.datasets[ds].notes['buggedpileup2017'] = True

    # set up jsons
    for y,ss in (2017, data_samples_2017 + auxiliary_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018):
        for s in ss:
            s.datasets[ds].json      = json_path('ana_%s.json'      % y)
            s.datasets[ds].json_10pc = json_path('ana_%s_10pc.json' % y)
            s.datasets[ds].json_1pc  = json_path('ana_%s_1pc.json'  % y)

########################################################################

if __name__ == '__main__':
    main(registry)

    import sys, re
    from pprint import pprint
    from JMTucker.Tools import DBS, colors
    from JMTucker.Tools.general import popen

    if 0:
        for year in 2017, 2018:
            for line in file(str(year)):
                if line.startswith('/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S'):
                    model = 'mfv_neu'
                elif line.startswith('/StopStopbarTo2Dbar2D'):
                    model = 'mfv_stopdbardbar'
                else:
                    print 'unrecognized line %r' % line
                    continue
                dataset = line.strip()
                mass, tau_s = re.search(r'M-(\d+)_CTau-(.*)_Tune', line).groups()
                mass, tau, tau_unit = int(mass), int(tau_s[:-2]), tau_s[-2:]
                if tau_unit == 'mm':
                    tau *= 1000
                else:
                    assert tau_unit == 'um'
                if mass in [400,600,800,1200,1600,3000] and tau in [100,300,1000,10000,30000]:
                    nevents = DBS.numevents_in_dataset(dataset)
                    print "    MCSample('%s_tau%06ium_M%04i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)

    if 0:
        for s in all_signal_samples_2017 + all_signal_samples_2018:
            l = DBS.datasets('/%s/*/MINIAODSIM' % s.primary_dataset)
            if len(l) == 1:
                nevents = DBS.numevents_in_dataset(l[0])
                print "_adbp('miniaod', '%s', %i)" % (l[0], nevents)
            else:
                print colors.boldred('no miniaod for %s' % s.name)

    if 0:
        for s in qcd_samples_2017 + ttbar_samples_2017 + qcd_samples_2018 + ttbar_samples_2018 + StealthSHH_samples_2017 + StealthSYY_samples_2017 + StealthSHH_samples_2018 + StealthSYY_samples_2018:
            s.set_curr_dataset('miniaod')
            il = s.int_lumi_orig / 1000
            nfn = len(s.filenames)
            print s.name, nfn, il, '->', int(400/il*nfn), int(400/il*s.nevents_orig)
