import { ethers } from "ethers";
import { useState } from "react";

import contractAddresses from "../chain-info/deployments/map.json";
import contractAbi from "../chain-info/contracts/crowdFunding2.json";

export function useGetCampaigns() {
  const [campaigns, setCampaigns] = useState([]);

  async function getCampaigns() {
    try {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const contract = contractAddresses["5"]["UpgradeableProxy"][0];
      const crowdfunding = contractAbi.abi;

      const crowdfundingInstance = new ethers.Contract(
        contract,
        crowdfunding,
        provider
      );

      const campaignsFromContract = await crowdfundingInstance.getCampaigns();
      console.log(campaignsFromContract);
      setCampaigns(campaignsFromContract);
    } catch (err) {
      console.log(err);
    }
  }

  return { campaigns, getCampaigns };
}
