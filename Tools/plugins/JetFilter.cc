#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/GeneratorProducts/interface/GenLumiInfoHeader.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

class JMTJetFilter : public edm::EDFilter {
public:
  explicit JMTJetFilter(const edm::ParameterSet&);
private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<pat::JetCollection> jets_token;

  const int min_njets;
  const double min_pt_for_ht;
  const double max_pt_for_ht;
  const double min_ht;
  const edm::EDGetTokenT<GenLumiInfoHeader> gen_lumi_header_token; // for randpar parsing
  const bool parse_randpars;
  //const int randpar_mass;
  const int randpar_mstop;
  const int randpar_mso;
  const std::string(randpar_ctau);
  //const std::string(randpar_dcay);
  const bool debug;
};

JMTJetFilter::JMTJetFilter(const edm::ParameterSet& cfg)
  : jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_pt_for_ht(cfg.getParameter<double>("min_pt_for_ht")),
    max_pt_for_ht(cfg.getParameter<double>("max_pt_for_ht")),
    min_ht(cfg.getParameter<double>("min_ht")),
    gen_lumi_header_token(consumes<GenLumiInfoHeader, edm::InLumi>(edm::InputTag("generator"))),
    parse_randpars(cfg.getParameter<bool>("parse_randpars")),
    //randpar_mass(cfg.getParameter<int>("randpar_mass")),
    randpar_mstop(cfg.getParameter<int>("randpar_mstop")),
    randpar_mso(cfg.getParameter<int>("randpar_mso")),
    randpar_ctau(cfg.getParameter<std::string>("randpar_ctau")),
    //randpar_dcay(cfg.getParameter<std::string>("randpar_dcay")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
}

bool JMTJetFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  std::cout << "in MFVEventFilter::filter" << std::endl;

  const edm::LuminosityBlock& lumi = event.getLuminosityBlock();

  // If pertinent, parse randpar configuration
  // the randpar filter WILL supersede the base eventFilter. Thus, only one filter is allowed to be applied
  if (parse_randpars) {
    std::cout << "in MFVEventFilter::filter parse_randpars" << std::endl;

    edm::Handle<GenLumiInfoHeader> gen_header;
    lumi.getByToken(gen_lumi_header_token, gen_header);

    std::string rp_config_desc = gen_header->configDescription();
    std::string str_mstop = std::to_string(randpar_mstop);
    std::string str_mso = std::to_string(randpar_mso);
    std::string str_ctau = randpar_ctau;
    //std::string str_dcay = randpar_dcay;

    std::string comp_string_SHH = "StealthSHH_2t4b_mStop-300to1400_mSo-lowandhigh_ctau-0p01to1000_" + str_mstop + "_" + str_mso + "_" + str_ctau;
    std::string comp_string_SYY = "StealthSYY_2t6j_mStop-300to1500_mSo-lowandhigh_ctau-0p01to1000_" + str_mstop + "_" + str_mso + "_" + str_ctau;
    if (not (comp_string_SHH == rp_config_desc || comp_string_SYY == rp_config_desc)) {
      //std::cout<<rp_config_desc<<'\n';
      //std::cout<<comp_string_SYY<<'\n';
      return false;
    }
    else {
      //std::cout<<'p';
      return true;
    }
  }


  double ht = 0;
  for (const pat::Jet& jet : *jets) {
    const double pt = jet.pt();
    if (pt > min_pt_for_ht && pt < max_pt_for_ht)
      ht += pt;
  }

  if (debug) printf("JetFilter: njets: %lu  ht: %f\n", jets->size(), ht);

  return
    int(jets->size()) >= min_njets && 
    ht >= min_ht;
}

DEFINE_FWK_MODULE(JMTJetFilter);
