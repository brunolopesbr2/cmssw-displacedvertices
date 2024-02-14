import FWCore.ParameterSet.Config as cms

jmtJetFilter = cms.EDFilter('JMTJetFilter',
                            jets_src = cms.InputTag('selectedPatJets'),
                            min_njets = cms.int32(4),
                            min_pt_for_ht = cms.double(40),
                            max_pt_for_ht = cms.double(1e9),
                            min_ht = cms.double(1000),
                            parse_randpars = cms.bool(False),
                            randpar_mass = cms.int32(-1),
                            randpar_mstop = cms.int32(-1),
                            randpar_mso = cms.int32(-1),
                            randpar_ctau = cms.string(''),
                            randpar_dcay = cms.string(''),
                            debug = cms.untracked.bool(False),
                            )
