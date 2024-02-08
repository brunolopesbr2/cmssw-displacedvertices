import FWCore.ParameterSet.Config as cms

#def setup_event_filter(process,
#                       path_name='pevtsel',
#                       trig_filt_name = 'triggerFilter',
#                       event_filter = False,
#                       event_filter_jes_mult = 2,
#                       event_filt_name = 'jetFilter',
#                       input_is_miniaod = False,
#                       ):

def setup_event_filter(process,
                       path_name='pevtsel',
                       trigger_filter = True,
                       trig_filt_name = 'mfvTriggerFilter',
                       event_filter = False,
                       event_filter_jes_mult = 2,
                       event_filt_name = 'mfvEventFilter',
                       event_filter_require_vertex = True,
                       rp_filter = False,
                       rp_mode = None,
                       #rp_mass = -1,
                       rp_mstop = -1,
                       rp_mso = -1,
                       rp_ctau = '',
                       #rp_dcay = '',
                       input_is_miniaod = False,
                       sequence_name = 'mfvEventFilterSequence',
                       name_ex = None,
                       ):


    if rp_mode :
        event_filter = True
        event_filter_require_vertex = False
        event_filter_jes_mult = 0
        rp_filter = True

        rp_mode_list = rp_mode.split('_')
        rp_mstop = int(rp_mode_list[1])
        rp_mso = int(rp_mode_list[2])
        rp_ctau = str(rp_mode_list[3])

    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    triggerFilter = hltHighLevel.clone()
    setattr(process, trig_filt_name, triggerFilter)
    triggerFilter.HLTPaths = [
        "HLT_PFHT800_v*",
        "HLT_PFHT900_v*",
        "HLT_PFJet450_v*",
        "HLT_AK8PFJet450_v*",
        ]
    triggerFilter.andOr = True # = OR
    triggerFilter.throw = False

    overall = triggerFilter

    if event_filter:
        if not input_is_miniaod and not hasattr(process, 'patJets'):
            raise NotImplementedError('need to understand how to include pat_tuple jets_only here')
        elif event_filter == 'HT OR bjets OR displaced dijet':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterHTORBjetsORDisplacedDijet as eventFilter
        elif event_filter == 'bjets OR displaced dijet veto HT':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterBjetsORDisplacedDijetVetoHT as eventFilter
        elif event_filter is True:
            if rp_filter:
                from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterRandomParameters as eventFilter
            else :
                from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilter as eventFilter
        elif event_filter is not False:
            raise ValueError('event_filter must be one of ("jets only", "leptons only", "HT OR bjets OR displaced dijet", "bjets OR displaced dijet veto HT", True, False)')

        from JMTucker.Tools.JetFilter_cfi import jmtJetFilter as jetFilter
        if input_is_miniaod:
            jetFilter.jets_src = 'slimmedJets'
        setattr(process, event_filt_name, jetFilter)

        if rp_filter:
            print "In EventFilter.py conditional"
            #eventFilter.randpar_mass = rp_mass
            eventFilter.randpar_mstop = rp_mstop
            eventFilter.randpar_mso = rp_mso
            eventFilter.randpar_ctau = rp_ctau
            #eventFilter.randpar_dcay = rp_dcay
            eventFilter.parse_randpars = True

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as jetShifter
            if input_is_miniaod:
                jetShifter.jets_src = 'slimmedJets'
            jetShifter.mult = event_filter_jes_mult
            jetShifter_name = event_filt_name + 'JESUncUp%i' % event_filter_jes_mult
            jetFilter.jets_src = jetShifter_name
            setattr(process, jetShifter_name, jetShifter)

            overall *= jetShifter * jetFilter
        else:
            overall *= jetFilter
            
    if hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))

    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
