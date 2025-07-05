/**
 * React Notion X Integration Component
 * Renders Notion-style content for CrewAI agent outputs and documentation
 */

import React from 'react';
import { NotionRenderer as NotionRendererBase } from 'react-notion-x';
import { Code } from 'react-notion-x/build/third-party/code';
import { Collection } from 'react-notion-x/build/third-party/collection';
import { Equation } from 'react-notion-x/build/third-party/equation';
import { Modal } from 'react-notion-x/build/third-party/modal';
import { Pdf } from 'react-notion-x/build/third-party/pdf';
import { Tweet } from 'react-notion-x/build/third-party/tweet';
import dynamic from 'next/dynamic';
import { ExtendedRecordMap } from 'notion-types';

// Dynamically import heavy components
const Mermaid = dynamic(() => import('react-notion-x/build/third-party/mermaid').then((m) => m.Mermaid), {
  ssr: false,
});

interface NotionRendererProps {
  recordMap: ExtendedRecordMap;
  fullPage?: boolean;
  darkMode?: boolean;
  previewImages?: boolean;
  showCollectionViewDropdown?: boolean;
  showTableOfContents?: boolean;
  minTableOfContentsItems?: number;
  defaultPageIcon?: string;
  defaultPageCover?: string;
  defaultPageCoverPosition?: number;
  className?: string;
  bodyClassName?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  pageTitle?: string;
  pageDescription?: string;
  pageImage?: string;
  pageCover?: string;
  disableHeader?: boolean;
  mapPageUrl?: (pageId: string) => string;
  mapImageUrl?: (url: string, block: any) => string;
  searchNotion?: (params: any) => Promise<any>;
  isRedirectingToNotion?: boolean;
  rootPageId?: string;
  rootDomain?: string;
  onLoad?: () => void;
}

export const NotionRenderer: React.FC<NotionRendererProps> = ({
  recordMap,
  fullPage = false,
  darkMode = false,
  previewImages = true,
  showCollectionViewDropdown = true,
  showTableOfContents = false,
  minTableOfContentsItems = 3,
  defaultPageIcon = '📄',
  defaultPageCover,
  defaultPageCoverPosition = 0.3,
  className,
  bodyClassName,
  header,
  footer,
  pageTitle,
  pageDescription,
  pageImage,
  pageCover,
  disableHeader = false,
  mapPageUrl,
  mapImageUrl,
  searchNotion,
  isRedirectingToNotion = false,
  rootPageId,
  rootDomain,
  onLoad,
  ...props
}) => {
  const components = React.useMemo(
    () => ({
      Code,
      Collection,
      Equation,
      Modal,
      Pdf,
      Tweet,
      Mermaid,
    }),
    []
  );

  return (
    <div className={`notion-renderer ${className || ''}`}>
      {header}
      <NotionRendererBase
        recordMap={recordMap}
        fullPage={fullPage}
        darkMode={darkMode}
        previewImages={previewImages}
        showCollectionViewDropdown={showCollectionViewDropdown}
        showTableOfContents={showTableOfContents}
        minTableOfContentsItems={minTableOfContentsItems}
        defaultPageIcon={defaultPageIcon}
        defaultPageCover={defaultPageCover}
        defaultPageCoverPosition={defaultPageCoverPosition}
        bodyClassName={bodyClassName}
        disableHeader={disableHeader}
        mapPageUrl={mapPageUrl}
        mapImageUrl={mapImageUrl}
        searchNotion={searchNotion}
        isRedirectingToNotion={isRedirectingToNotion}
        rootPageId={rootPageId}
        rootDomain={rootDomain}
        components={components}
        onLoad={onLoad}
        {...props}
      />
      {footer}
    </div>
  );
};

export default NotionRenderer;